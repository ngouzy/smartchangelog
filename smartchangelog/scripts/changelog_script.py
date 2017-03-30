import argparse

from smartchangelog.gitcmd import log
from smartchangelog import __version__
from smartchangelog.changelog import Changelog
from smartchangelog.commit import Commit


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart changelog report",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", help="print smartchangelog version number", action="version",
                        version=__version__)

    parser.add_argument("-r", "--range", help="revision range (in the same meaning than git log command)")
    parser.add_argument("-g", "--groupby", help="list of criteria", nargs="*")

    args = parser.parse_args()

    gitlog = log(revision_range=args.range)

    changelog = Changelog.parse(gitlog)

    if args.groupby:
        criteria = tuple((Commit.property(criterion) for criterion in args.groupby))
    else:
        criteria = ()

    node = changelog.groupby(*criteria)
    print(node.report())
    exit(0)


if __name__ == "__main__":
    main()
