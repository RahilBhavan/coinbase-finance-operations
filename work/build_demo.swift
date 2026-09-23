import Foundation
import AVFoundation
import AppKit

let root = CommandLine.arguments[1]
let output = URL(fileURLWithPath: root + "/artifacts/demo.mp4")
try? FileManager.default.removeItem(at: output)
let writer = try AVAssetWriter(outputURL: output, fileType: .mp4)
let settings: [String: Any] = [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: 1280, AVVideoHeightKey: 720]
let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
    kCVPixelBufferWidthKey as String: 1280,
    kCVPixelBufferHeightKey as String: 720
])
writer.add(input); writer.startWriting(); writer.startSession(atSourceTime: .zero)

let slides: [(String, [String])] = [
    ("Settlement exception desk", ["Synthetic x402 exact workflow on Base Sepolia", "Decision: retain FIFO for the initial scenario", "65 events | 16 incidents | 0 control failures"]),
    ("Timeout is not failure", ["The settlement request timed out", "Outcome remains unknown", "Reconcile the original attempt", "Never trigger another charge automatically"]),
    ("Late payment, missing delivery", ["Late evidence attaches to the original attempt", "Payment state: observed", "Delivery state: prepared", "Recover the persisted report; do not charge again"]),
    ("Refund reservation control", ["Approval reserves refundable balance", "Unknown submission keeps the reservation", "Completed plus reserved cannot exceed capture", "Concurrent excess request is blocked"]),
    ("Policy comparison", ["FIFO overdue cases: 6", "Deadline-first overdue cases: 6", "Weighted delay improved, primary count did not", "The 15% adoption gate was not met"]),
    ("Recommendation and limits", ["Keep FIFO as the working baseline", "Test a narrow SLA-window hybrid next", "All data and timings are simulated", "No live wallet, payment, Coinbase system, or savings claim"]),
]

func pixelBuffer(title: String, lines: [String]) -> CVPixelBuffer? {
    var buffer: CVPixelBuffer?
    CVPixelBufferCreate(kCFAllocatorDefault, 1280, 720, kCVPixelFormatType_32ARGB,
                        [kCVPixelBufferCGImageCompatibilityKey: true,
                         kCVPixelBufferCGBitmapContextCompatibilityKey: true] as CFDictionary, &buffer)
    guard let pb = buffer else { return nil }
    CVPixelBufferLockBaseAddress(pb, [])
    let ctx = CGContext(data: CVPixelBufferGetBaseAddress(pb), width: 1280, height: 720,
                        bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(pb),
                        space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)!
    ctx.setFillColor(NSColor(calibratedRed: 0.96, green: 0.98, blue: 0.99, alpha: 1).cgColor); ctx.fill(CGRect(x: 0, y: 0, width: 1280, height: 720))
    ctx.setFillColor(NSColor(calibratedRed: 0.08, green: 0.23, blue: 0.36, alpha: 1).cgColor); ctx.fill(CGRect(x: 0, y: 630, width: 1280, height: 90))
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = NSGraphicsContext(cgContext: ctx, flipped: false)
    let titleAttrs: [NSAttributedString.Key: Any] = [.font: NSFont.boldSystemFont(ofSize: 38), .foregroundColor: NSColor.white]
    NSString(string: title).draw(at: NSPoint(x: 68, y: 654), withAttributes: titleAttrs)
    let lineAttrs: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: 30, weight: .medium), .foregroundColor: NSColor(calibratedRed: 0.09, green: 0.13, blue: 0.17, alpha: 1)]
    for (i, line) in lines.enumerated() { NSString(string: line).draw(at: NSPoint(x: 100, y: 510 - i * 88), withAttributes: lineAttrs) }
    let foot: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: 18), .foregroundColor: NSColor.darkGray]
    NSString(string: "SIMULATED DATA - NO ACTIONS EXECUTED").draw(at: NSPoint(x: 68, y: 40), withAttributes: foot)
    NSGraphicsContext.restoreGraphicsState(); CVPixelBufferUnlockBaseAddress(pb, [])
    return pb
}

let queue = DispatchQueue(label: "demo.writer")
input.requestMediaDataWhenReady(on: queue) {
    var frame = 0
    while input.isReadyForMoreMediaData && frame < 180 {
        let slide = slides[min(frame / 30, slides.count - 1)]
        if let pb = pixelBuffer(title: slide.0, lines: slide.1) {
            adaptor.append(pb, withPresentationTime: CMTime(value: CMTimeValue(frame), timescale: 1))
        }
        frame += 1
    }
    if frame >= 180 {
        input.markAsFinished()
        writer.finishWriting { exit(writer.status == .completed ? 0 : 1) }
    }
}
dispatchMain()
