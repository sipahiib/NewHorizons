import AppKit
import Foundation

let out = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
try FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)

func make(_ name: String, _ w: Int, _ h: Int, _ paint: (CGContext) -> Void) {
    let r = NSBitmapImageRep(
        bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0
    )!
    NSGraphicsContext.saveGraphicsState()
    let c = NSGraphicsContext(bitmapImageRep: r)!
    NSGraphicsContext.current = c
    c.cgContext.clear(CGRect(x: 0, y: 0, width: w, height: h))
    paint(c.cgContext)
    NSGraphicsContext.restoreGraphicsState()
    try! r.representation(using: .png, properties: [:])!.write(to: out.appendingPathComponent(name))
}

func label(_ s: String, _ x: CGFloat, _ y: CGFloat, _ size: CGFloat) {
    NSAttributedString(string: s, attributes: [
        .font: NSFont.boldSystemFont(ofSize: size),
        .foregroundColor: NSColor.white
    ]).draw(at: NSPoint(x: x, y: y))
}

func title(_ name: String, _ text: String) {
    make(name, 1920, 1080) { c in
        c.setFillColor(NSColor(calibratedRed: 0.025, green: 0.106, blue: 0.137, alpha: 0.62).cgColor)
        c.fill(CGRect(x: 65, y: 900, width: 1460, height: 130))
        label(text, 100, 936, 48)
    }
}

title("title-bepicolombo.png", "BEPICOLOMBO ENTERS MERCURY ORBIT")
title("title-edith.png", "UK AI BREAST SCREENING TRIAL")

make("subscribe.png", 1920, 1080) { c in
    c.setFillColor(NSColor(calibratedRed: 0.025, green: 0.106, blue: 0.137, alpha: 0.72).cgColor)
    c.fill(CGRect(x: 1210, y: 80, width: 650, height: 220))
    label("YouTube", 1250, 220, 40)
    label("Like • Subscribe • Join in", 1250, 160, 31)
    label("SUBSCRIBE", 1250, 105, 36)
}

make("closing-bg.png", 1920, 1080) { c in
    c.setFillColor(NSColor(calibratedRed: 0.035, green: 0.11, blue: 0.15, alpha: 1).cgColor)
    c.fill(CGRect(x: 0, y: 0, width: 1920, height: 1080))
}

make("closing-panel.png", 1920, 1080) { c in
    c.setFillColor(NSColor(calibratedRed: 0.3, green: 0.45, blue: 0.5, alpha: 0.32).cgColor)
    c.fill(CGRect(x: 380, y: 265, width: 1160, height: 550))
    label("LIKE • SUBSCRIBE", 670, 570, 72)
    label("SUBSCRIBE", 820, 390, 42)
}

make("bell.png", 180, 180) { c in
    c.setFillColor(NSColor.systemYellow.cgColor)
    c.fillEllipse(in: CGRect(x: 44, y: 55, width: 92, height: 90))
    c.fill(CGRect(x: 44, y: 45, width: 92, height: 40))
    c.fillEllipse(in: CGRect(x: 75, y: 23, width: 30, height: 30))
}
