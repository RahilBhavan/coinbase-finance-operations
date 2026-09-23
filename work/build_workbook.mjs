import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = process.argv[2];
const outDir = `${root}/artifacts`;
const userOut = `${root}/outputs`;
const oracle = JSON.parse(await fs.readFile(`${root}/data/incidents-v1.oracle.json`, "utf8"));
const policyDocument = JSON.parse(await fs.readFile(`${root}/artifacts/generated/policy-results.json`, "utf8"));
const policies = policyDocument.policies;

const wb = Workbook.create();
const summary = wb.worksheets.add("Summary");
const recon = wb.worksheets.add("Reconciliation");
const incidents = wb.worksheets.add("Incident Oracle");
const policy = wb.worksheets.add("Policy Results");
for (const sh of [summary, recon, incidents, policy]) sh.showGridLines = false;

const navy = "#153A5B", blue = "#E8F1F8", red = "#FCE8E6", ink = "#17212B", line = "#D9E1E8";
summary.getRange("A2:F2").merge();
summary.getRange("A2").values = [["Settlement exception reconciliation"]];
summary.getRange("A2:F2").format.font = {name:"Arial", size:16, bold:true, color:ink};
summary.getRange("A3:F3").merge();
summary.getRange("A3").values = [["Synthetic fixed-price x402 incidents | Prepared 2026-09-20"]];
summary.getRange("A3:F3").format.font = {name:"Arial", size:10, italic:true, color:"#4E6475"};
summary.getRange("A5:B9").values = [
  ["Decision", "Retain FIFO for the initial scenario"],
  ["Reason", "Deadline-first did not reduce overdue case count"],
  ["Fixture cases", 16], ["Events", 65], ["Control failures", 0]
];
summary.getRange("A5:A9").format = {fill:navy, font:{name:"Arial", size:10, bold:true, color:"#FFFFFF"}};
summary.getRange("B5:B9").format = {fill:blue, font:{name:"Arial", size:10, color:ink}, wrapText:true};
summary.getRange("A5:B9").format.borders = {preset:"all", style:"thin", color:line};
summary.getRange("D5:F5").values = [["Metric","FIFO","Deadline-first"]];
const keys = [
  ["Overdue cases","overdue_count"], ["Median delay (min)","median_resolution_delay_minutes"],
  ["P95 delay (min)","p95_resolution_delay_minutes"], ["Value-weighted overdue minutes","value_weighted_overdue_minutes"],
  ["Unfinished cases","unfinished_count"]
];
summary.getRange("D6:F10").values = keys.map(([label,key]) => [label, policies.fifo[key], policies.deadline_first[key]]);
summary.getRange("D5:F5").format = {fill:navy, font:{name:"Arial", size:10, bold:true, color:"#FFFFFF"}, horizontalAlignment:"center"};
summary.getRange("D5:F10").format.borders = {preset:"all", style:"thin", color:line};
summary.getRange("E6:F10").format.numberFormat = "#,##0.0";
summary.getRange("A12:F14").merge();
summary.getRange("A12").values = [["Interpretation: this scenario does not meet the predeclared 15% overdue-count improvement gate. Handling times and incident frequencies are simulated, so results do not establish operational savings or Coinbase policy."]];
summary.getRange("A12:F14").format = {fill:red, font:{name:"Arial", size:10, color:ink}, wrapText:true, verticalAlignment:"center"};
summary.getRange("A:F").format.font = {name:"Arial", size:10};
summary.getRange("A:A").format.columnWidth = 24; summary.getRange("B:B").format.columnWidth = 34;
summary.getRange("C:C").format.columnWidth = 3; summary.getRange("D:D").format.columnWidth = 32;
summary.getRange("E:F").format.columnWidth = 18;

const headers = ["Fixture ID","Captured (atomic)","Reserved refund (atomic)","Completed refund (atomic)","Available refundable (atomic)","Check"];
recon.getRange("A2:F2").values = [headers];
const rows = oracle.cases.map(c => [c.fixture_id,c.expected_financials.captured_atomic,c.expected_financials.reserved_refund_atomic,c.expected_financials.completed_refund_atomic,null,null]);
recon.getRangeByIndexes(2,0,rows.length,6).values = rows;
for (let row=3; row<3+rows.length; row++) {
  recon.getRange(`E${row}`).formulas = [[`=B${row}-C${row}-D${row}`]];
  recon.getRange(`F${row}`).formulas = [[`=IF(E${row}<0,"FAIL","OK")`]];
}
recon.getRange("A2:F2").format = {fill:navy,font:{name:"Arial",size:10,bold:true,color:"#FFFFFF"},horizontalAlignment:"center",wrapText:true};
recon.getRange(`A2:F${2+rows.length}`).format.borders = {preset:"all",style:"thin",color:line};
recon.getRange(`B3:E${2+rows.length}`).format.numberFormat = "#,##0";
recon.getRange("A:F").format.font = {name:"Arial",size:10};
recon.getRange("A:A").format.columnWidth = 33; recon.getRange("B:E").format.columnWidth = 20; recon.getRange("F:F").format.columnWidth = 11;
recon.freezePanes.freezeRows(2);

incidents.getRange("A2:F2").values = [["Fixture ID","Category","Scenario","Payment state","Fulfillment state","Exception"]];
incidents.getRangeByIndexes(2,0,oracle.cases.length,6).values = oracle.cases.map(c => [c.fixture_id,c.category,c.scenario,c.expected_payment_state,c.expected_fulfillment_state,c.expected_exception_type || "none"]);
incidents.getRange("A2:F2").format = {fill:navy,font:{name:"Arial",size:10,bold:true,color:"#FFFFFF"},horizontalAlignment:"center"};
incidents.getRange(`A2:F${2+oracle.cases.length}`).format.borders = {preset:"all",style:"thin",color:line};
incidents.getRange("A:F").format.font = {name:"Arial",size:10};
incidents.getRange(`C3:F${2+oracle.cases.length}`).format.wrapText = true;
incidents.getRange(`A2:F${2+oracle.cases.length}`).format.rowHeight = 26;
incidents.getRange("A:A").format.columnWidth = 34; incidents.getRange("B:B").format.columnWidth = 14;
incidents.getRange("C:C").format.columnWidth = 38; incidents.getRange("D:E").format.columnWidth = 24; incidents.getRange("F:F").format.columnWidth = 40;
incidents.freezePanes.freezeRows(2);

policy.getRange("A2:J2").values = [["Policy","Overdue","Median delay","P95 delay","Weighted overdue","Unfinished","Unfinished value","Touches","Control failures","Workload hash"]];
policy.getRange("A3:J6").values = ["fifo","deadline_first","value_first","hybrid"].map(name => {
  const p=policies[name]; return [name,p.overdue_count,p.median_resolution_delay_minutes,p.p95_resolution_delay_minutes,p.value_weighted_overdue_minutes,p.unfinished_count,p.unfinished_value_atomic,p.touches,p.control_failures,p.workload_fingerprint];
});
policy.getRange("A2:J2").format = {fill:navy,font:{name:"Arial",size:10,bold:true,color:"#FFFFFF"},horizontalAlignment:"center",wrapText:true};
policy.getRange("A2:J6").format.borders = {preset:"all",style:"thin",color:line};
policy.getRange("A:J").format.font = {name:"Arial",size:10};
policy.getRange("A:A").format.columnWidth=18; policy.getRange("B:I").format.columnWidth=16; policy.getRange("J:J").format.columnWidth=38;

wb.recalculate();
const inspect = await wb.inspect({kind:"table", sheetId:"Summary", range:"A2:F14", include:"values,formulas", tableMaxRows:20, tableMaxCols:8});
console.log(inspect.ndjson);
const errors = await wb.inspect({kind:"match", searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options:{useRegex:true,maxResults:100}, summary:"formula error scan"});
console.log(errors.ndjson);
await fs.mkdir(`${root}/work/workbook-preview`, {recursive:true});
for (const name of ["Summary","Reconciliation","Incident Oracle","Policy Results"]) {
  const png = await wb.render({sheetName:name, autoCrop:"all", scale:1, format:"png"});
  await fs.writeFile(`${root}/work/workbook-preview/${name.replaceAll(" ","-")}.png`, new Uint8Array(await png.arrayBuffer()));
}
await fs.mkdir(outDir,{recursive:true}); await fs.mkdir(userOut,{recursive:true});
const blob = await SpreadsheetFile.exportXlsx(wb);
await blob.save(`${outDir}/reconciliation.xlsx`);
await blob.save(`${userOut}/reconciliation.xlsx`);
