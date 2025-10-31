// swift-tools-version:5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "wcdb-spm-prebuilt",
     platforms: [
        .iOS(.v12),
        // .watchOS(.v4),
        // .tvOS(.v12),
        .macOS(.v10_13),
        .macCatalyst(.v13),
    ],
    products: [
        .library(name: "WCDBSwift", targets: ["WCDBSwift"]),
        .library(name: "WCDBObjc", targets: ["WCDBObjc"]),
    ],
    targets: [
        .binaryTarget(
            name: "WCDBSwift",
            url: "https://github.com/0x1306a94/wcdb-spm-prebuilt/releases/download/storage.v2.1.14/WCDBSwift.xcframework.zip",
            checksum: "d485c7657145608969e11fdcbbf0da940c0d7831f05cd565888fa677c86b2a62"
        ),
        .binaryTarget(
            name: "WCDBObjc",
            url: "https://github.com/0x1306a94/wcdb-spm-prebuilt/releases/download/storage.v2.1.14/WCDBObjc.xcframework.zip",
            checksum: "dd9d15fa456d5c324dff9601f2b1f4cf3ed7420ce86ffb45a20dbea6b3f5b272"
        ),
    ]
)