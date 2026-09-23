#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <AppKit/AppKit.h>

CVPixelBufferRef makeFrame(NSString *title, NSArray<NSString *> *lines) {
    NSDictionary *attrs=@{(id)kCVPixelBufferCGImageCompatibilityKey:@YES,(id)kCVPixelBufferCGBitmapContextCompatibilityKey:@YES};
    CVPixelBufferRef pb=NULL; CVPixelBufferCreate(kCFAllocatorDefault,1280,720,kCVPixelFormatType_32ARGB,(__bridge CFDictionaryRef)attrs,&pb);
    CVPixelBufferLockBaseAddress(pb,0);
    CGContextRef ctx=CGBitmapContextCreate(CVPixelBufferGetBaseAddress(pb),1280,720,8,CVPixelBufferGetBytesPerRow(pb),CGColorSpaceCreateDeviceRGB(),kCGImageAlphaNoneSkipFirst);
    CGContextSetRGBFillColor(ctx,.96,.98,.99,1); CGContextFillRect(ctx,CGRectMake(0,0,1280,720));
    CGContextSetRGBFillColor(ctx,.08,.23,.36,1); CGContextFillRect(ctx,CGRectMake(0,630,1280,90));
    [NSGraphicsContext saveGraphicsState]; [NSGraphicsContext setCurrentContext:[NSGraphicsContext graphicsContextWithCGContext:ctx flipped:NO]];
    [title drawAtPoint:NSMakePoint(68,654) withAttributes:@{NSFontAttributeName:[NSFont boldSystemFontOfSize:38],NSForegroundColorAttributeName:NSColor.whiteColor}];
    NSDictionary *lineAttrs=@{NSFontAttributeName:[NSFont systemFontOfSize:30 weight:NSFontWeightMedium],NSForegroundColorAttributeName:[NSColor colorWithCalibratedRed:.09 green:.13 blue:.17 alpha:1]};
    for(NSUInteger i=0;i<lines.count;i++) [lines[i] drawAtPoint:NSMakePoint(100,510-i*88) withAttributes:lineAttrs];
    [@"SIMULATED DATA - NO ACTIONS EXECUTED" drawAtPoint:NSMakePoint(68,40) withAttributes:@{NSFontAttributeName:[NSFont systemFontOfSize:18],NSForegroundColorAttributeName:NSColor.darkGrayColor}];
    [NSGraphicsContext restoreGraphicsState]; CGContextRelease(ctx); CVPixelBufferUnlockBaseAddress(pb,0); return pb;
}

int main(int argc,const char *argv[]){ @autoreleasepool {
    NSString *root=[NSString stringWithUTF8String:argv[1]], *path=[root stringByAppendingPathComponent:@"work/demo.mov"];
    [[NSFileManager defaultManager] removeItemAtPath:path error:nil];
    NSError *err=nil; AVAssetWriter *writer=[[AVAssetWriter alloc] initWithURL:[NSURL fileURLWithPath:path] fileType:AVFileTypeQuickTimeMovie error:&err];
    NSDictionary *settings=@{AVVideoCodecKey:AVVideoCodecTypeAppleProRes422,AVVideoWidthKey:@1280,AVVideoHeightKey:@720};
    AVAssetWriterInput *input=[AVAssetWriterInput assetWriterInputWithMediaType:AVMediaTypeVideo outputSettings:settings];
    AVAssetWriterInputPixelBufferAdaptor *adaptor=[AVAssetWriterInputPixelBufferAdaptor assetWriterInputPixelBufferAdaptorWithAssetWriterInput:input sourcePixelBufferAttributes:@{(id)kCVPixelBufferPixelFormatTypeKey:@(kCVPixelFormatType_32ARGB),(id)kCVPixelBufferWidthKey:@1280,(id)kCVPixelBufferHeightKey:@720}];
    [writer addInput:input]; [writer startWriting]; [writer startSessionAtSourceTime:kCMTimeZero];
    NSArray *slides=@[
      @[@"Settlement exception desk",@[@"Synthetic x402 exact workflow on Base Sepolia",@"Decision: retain FIFO for the initial scenario",@"65 events | 16 incidents | 0 control failures"]],
      @[@"Timeout is not failure",@[@"The settlement request timed out",@"Outcome remains unknown",@"Reconcile the original attempt",@"Never trigger another charge automatically"]],
      @[@"Late payment, missing delivery",@[@"Late evidence attaches to the original attempt",@"Payment state: observed",@"Delivery state: prepared",@"Recover the persisted report; do not charge again"]],
      @[@"Refund reservation control",@[@"Approval reserves refundable balance",@"Unknown submission keeps the reservation",@"Completed plus reserved cannot exceed capture",@"Concurrent excess request is blocked"]],
      @[@"Policy comparison",@[@"FIFO overdue cases: 6",@"Deadline-first overdue cases: 6",@"Weighted delay improved, primary count did not",@"The 15% adoption gate was not met"]],
      @[@"Recommendation and limits",@[@"Keep FIFO as the working baseline",@"Test a narrow SLA-window hybrid next",@"All data and timings are simulated",@"No live wallet, payment, Coinbase system, or savings claim"]]
    ];
    for(int frame=0;frame<180;frame++){
      while(!input.readyForMoreMediaData) [NSThread sleepForTimeInterval:.01];
      NSArray *slide=slides[MIN(frame/30,5)]; CVPixelBufferRef pb=makeFrame(slide[0],slide[1]);
      [adaptor appendPixelBuffer:pb withPresentationTime:CMTimeMake(frame,1)]; CVPixelBufferRelease(pb);
    }
    [input markAsFinished]; dispatch_semaphore_t sem=dispatch_semaphore_create(0); [writer finishWritingWithCompletionHandler:^{dispatch_semaphore_signal(sem);}]; dispatch_semaphore_wait(sem,DISPATCH_TIME_FOREVER);
    if(writer.status!=AVAssetWriterStatusCompleted){ NSLog(@"%@",writer.error); return 1; }
  } return 0; }
