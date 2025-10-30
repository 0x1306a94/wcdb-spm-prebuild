#!/usr/bin/env python3
import argparse
import subprocess
import os
from pathlib import Path
import time
import shutil

def run_command(cmd, cwd=None):
    """运行命令并实时输出日志"""
    print(f"\n[cmd] {' '.join(cmd)}\n")
    process = subprocess.Popen(
        cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, cmd)


def archive_target(project_file, scheme, configuration, destination, archive_path, use_xcbeautify, extra_args=None):
    """执行 archive 构建"""
    cmd = [
        "xcodebuild",
        "archive",
        "-project", str(project_file),
        "-scheme", scheme,
        "-configuration", configuration,
        "-destination", destination,
        "-archivePath", str(archive_path),
        "SKIP_INSTALL=NO",
    ]

    if extra_args:
        cmd += extra_args

    if use_xcbeautify:
        print(f"\n[cmd] {' '.join(cmd)}\n")
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["xcbeautify"], stdin=p1.stdout)
        p1.stdout.close()
        p2.communicate()
        if p1.wait() != 0:
            raise subprocess.CalledProcessError(p1.returncode, cmd)
    else:
        run_command(cmd)


def create_xcframework(archives, output_dir, framework_name):
    """创建 XCFramework"""
    cmd = ["xcodebuild", "-create-xcframework"]
    for arch in archives:
        cmd += ["-archive", str(arch), "-framework",
                f"{framework_name}.framework"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{framework_name}.xcframework"
    if os.path.exists(output_path):
        print(f"[*] Removing existing xcframework: {output_path}")
        shutil.rmtree(output_path)

    cmd += ["-output", str(output_path)]
    run_command(cmd)
    print(f"\n✅ Created XCFramework: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Build WCDB (or WCDBCpp/Objc/Swift) into XCFramework")
    parser.add_argument("--scheme", choices=["WCDB", "WCDBCpp", "WCDBObjc", "WCDBSwift"],
                        required=True, help="Scheme to build (required)")
    parser.add_argument("--configuration", default="Release",
                        help="Build configuration (default: Release)")
    parser.add_argument("--project", default="src/WCDB.xcodeproj",
                        help="Relative path to .xcodeproj")
    parser.add_argument("--output", default="build_out",
                        help="Output directory (default: build_out)")
    parser.add_argument("--platforms", nargs="+", choices=["ios", "ios-simulator", "macos", "macos-catalyst", "all"],
                        default=["all"], help="Platforms to build (default: all)")
    parser.add_argument("--no-xcframework", action="store_true",
                        help="Skip creating XCFramework")
    parser.add_argument("--xcbeautify", action="store_true",
                        help="Use xcbeautify for build output")

    args = parser.parse_args()

    start_time = time.time()

    repo_root = Path(__file__).resolve().parent
    project_file = repo_root / args.project
    build_out_dir = repo_root / args.output
    archives_dir = build_out_dir / "archives"
    xcframeworks_dir = build_out_dir / "xcframeworks"

    print(f"[*] REPO_ROOT_DIR: {repo_root}")
    print(f"[*] XCODE_PROJECT_FILE: {project_file}")
    print(f"[*] BUILD_OUT_DIR: {build_out_dir}")
    print(f"[*] BUILD_ARCHIVES_DIR: {archives_dir}\n")

    extra_args_map = {
        "WCDBSwift": ["BUILD_LIBRARY_FOR_DISTRIBUTION=YES"],
        "WCDBObjc": [],
        "WCDBCpp": [],
        "WCDB": []
    }

    destinations = {
        "ios": "generic/platform=iOS",
        "ios-simulator": "generic/platform=iOS Simulator",
        "macos": "generic/platform=macOS",
        "macos-catalyst": "generic/platform=macOS,variant=Mac Catalyst"
    }

    if "all" in args.platforms:
        platforms = list(destinations.keys())
    else:
        platforms = args.platforms

    archives_dir.mkdir(parents=True, exist_ok=True)
    archives = []

    for platform in platforms:
        print(f"\n🚧 Building {args.scheme} ({platform})...")
        archive_path = archives_dir / f"{args.scheme}-{platform}"
        archive_target(
            project_file,
            args.scheme,
            args.configuration,
            destinations[platform],
            archive_path,
            args.xcbeautify,
            extra_args=extra_args_map.get(args.scheme, [])
        )
        archives.append(archive_path.with_suffix(".xcarchive"))

    if not args.no_xcframework:
        print(f"\n🧩 Creating XCFramework for {args.scheme} ...")
        create_xcframework(archives, xcframeworks_dir, args.scheme)
    else:
        print("\n⚙️ Skipped XCFramework creation (--no-xcframework).")

    end_time = time.time()
    elapsed = end_time - start_time
    mins, secs = divmod(int(elapsed), 60)
    print(f"\n⏱ Total elapsed time: {mins} min {secs} sec ({elapsed:.2f} s)")


if __name__ == "__main__":
    main()
