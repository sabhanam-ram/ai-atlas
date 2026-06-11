"""CLI: python -m kb <new|fetch|build|validate>"""
from __future__ import annotations

import argparse
import sys


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="kb", description="learning-ai knowledge-base pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="scaffold a video folder + meta.json (and fetch transcript)")
    p_new.add_argument("url")
    p_new.add_argument("--no-fetch", action="store_true", help="do not fetch the transcript")
    p_new.add_argument("--channel", help="override the channel slug")

    p_fetch = sub.add_parser("fetch", help="(re)fetch the transcript for an existing video")
    p_fetch.add_argument("url")
    p_fetch.add_argument("--channel", help="override the channel slug")

    p_build = sub.add_parser("build", help="render content/ -> docs/")
    p_build.add_argument("--clean", action="store_true", help="wipe docs/ before rebuilding")

    sub.add_parser("validate", help="check meta.json + registry + internal links")

    args = parser.parse_args(argv)

    if args.cmd == "new":
        from . import scaffold
        scaffold.new(args.url, do_fetch=not args.no_fetch, channel=args.channel)
    elif args.cmd == "fetch":
        from . import scaffold
        scaffold.refetch(args.url, channel=args.channel)
    elif args.cmd == "build":
        from . import render
        render.build(clean=args.clean)
    elif args.cmd == "validate":
        from .validate import validate
        errors, warnings = validate()
        for w in warnings:
            print(f"warning: {w}")
        for e in errors:
            print(f"ERROR: {e}")
        if errors:
            print(f"validate: FAILED ({len(errors)} error(s), {len(warnings)} warning(s))")
            return 1
        print(f"validate: OK ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
