import AppKit
import Foundation
let dir = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
func make(_ name: String, _ paint: (CGContext) -> Void) {
 let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: 1080, pixelsHigh: 1920, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
 NSGraphicsContext.saveGraphicsState(); let ctx = NSGraphicsContext(bitmapImageRep: rep)!; NSGraphicsContext.current = ctx
 ctx.cgContext.clear(CGRect(x:0,y:0,width:1080,height:1920)); paint(ctx.cgContext)
 NSGraphicsContext.restoreGraphicsState(); try! rep.representation(using: .png, properties: [:])!.write(to: dir.appendingPathComponent(name))
}
func label(_ text: String, _ y: CGFloat, _ size: CGFloat) {
 let attrs: [NSAttributedString.Key:Any] = [.font:NSFont.boldSystemFont(ofSize:size), .foregroundColor:NSColor.white]
 let str=NSAttributedString(string:text,attributes:attrs); str.draw(at:NSPoint(x:(1080-str.size().width)/2,y:y))
}
make("title.png") { c in c.setFillColor(NSColor(calibratedWhite:0,alpha:0.64).cgColor); c.fill(CGRect(x:70,y:1580,width:940,height:130)); label("SCOTLAND’S FLOW COUNTRY",1620,48) }
make("cta.png") { _ in label("YouTube  @newhorizons_21",320,36); label("Instagram  Like and follow",270,36) }
