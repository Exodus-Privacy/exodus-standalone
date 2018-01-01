import sys
from exodus_core.analysis.static_analysis import StaticAnalysis


if __name__ == '__main__':
    analysis = StaticAnalysis(sys.argv[1])
    analysis.load_trackers_signatures()
    analysis.print_apk_infos()
    analysis.print_embedded_trackers()
