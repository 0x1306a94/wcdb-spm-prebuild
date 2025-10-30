// swift-tools-version:5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "wcdb-spm-prebuilt",
     platforms: [
        .macOS(.v10_13),
        // .watchOS(.v4),
        // .tvOS(.v12),
        .iOS(.v12),
    ],
    products: [
        .library(name: "WCDBSwift", targets: ["WCDBSwift"]),
        .library(name: "WCDBObjc", targets: ["WCDBObjc"]),
    ],
    targets: [
        .binaryTarget(
            name: "WCDBSwift",
            url: "__WCDBSwift_DOWNLOAD_URL__",
            checksum: "__WCDBSwift_CHECKSUM__"
        ),
        .binaryTarget(
            name: "WCDBObjc",
            url: "__WCDBObjc_DOWNLOAD_URL__",
            checksum: "__WCDBObjc_CHECKSUM__"
        ),
    ]
)