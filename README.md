# wcdb-spm-prebuild

This repository provides **prebuilt XCFrameworks** of [WCDB](https://github.com/Tencent/wcdb) for Swift Package Manager (SPM).  
It allows you to use WCDB without compiling its C/C++ core every time. The binaries include prebuilt `sqlcipher` and any applied patches.

| Platform          | Architectures         | Minimal Deployment Target |
|------------------|----------------------|---------------------------|
| macOS             | x86_64 arm64        | 10.13                     |
| mac Catalyst      | x86_64 arm64        | 10.13 (iOS ABI 13.1)      |
| iOS               | arm64               | 11.0                      |
| iOS Simulator     | x86_64 arm64        | 11.0                      |

## Usage

Add the following line to your `Package.swift` dependencies:

```swift
.package(
    name: "WCDB",
    url: "https://github.com/0x1306a94/wcdb-spm-prebuild", 
    from: "2.1.14"
)
```

Then add `WCDB` as a dependency for your target:
```swift
.target(
    name: "MyApp",
    dependencies: [
       .product(name: "WCDBSwift", package: "WCDB"),
       // or
       .product(name: "WCDBObjc", package: "WCDB"),
    ]
)
```

## Credits:

- [https://github.com/Tencent/wcdb](https://github.com/Tencent/wcdb)