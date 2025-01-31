import argparse
import datetime
import statistics
import math
import speedtest
import hurry.filesize as hf

def quick_test(args: argparse.Namespace):
    print("Running a quick speedtest.")
    s = speedtest.Speedtest()
    results = s.test_small(True)
    print(f"{results[2]:.2f} Mbps\t{hf.size(results[0], system = hf.alternative)} in {results[1]:.1f} s")

def test(args: argparse.Namespace):
    test_start = datetime.datetime.now()
    tests_number = args.number[0]
    tests = []
    s = speedtest.Speedtest()

    if not args.silent:
        print(f"Running {tests_number} test(s). Using {args.size} filesize.")
        print("Tests completed: ", end = '', flush = True)
    
    for i in range(tests_number):
        match args.size:
            case "small":
                tests.append(s.test_small(verbose = True))
            case "medium":
                tests.append(s.test_medium(verbose = True))
            case "large":
                tests.append(s.test_large(verbose = True))
        if not args.silent:
            print(f"{i + 1}", end='\n' if i + 1 == tests_number else ' ', flush = True)
    #test_end = datetime.datetime.now()

    output = f">>> Began test at {test_start:%d-%m-%Y %H:%M:%S}\n"
    for n, t in enumerate(tests):
        output += f"Test {n+1:>{math.floor(math.log10(tests_number)) + 1}}:\tSpeed: {t[2]:.2f} Mbps\tFilesize: {hf.size(t[0], system = hf.alternative)}\tDuration: {t[1]:.1f} s\n"
    output += '=' * 10 + ' '
    mean = statistics.mean(t[2] for t in tests)
    output += f"Average: {mean:.2f} Mbps\tTests completed: {tests_number}"
    output += ' ' + '=' * 10

    if args.logfile is not None:
        with open(args.logfile, 'a') as f:
            f.write(output + '\n')
        if not args.silent:
            print(f"Tests saved to logfile: {args.logfile}")
    if not args.silent:
        print(output)

def main():
    parser = argparse.ArgumentParser(
        prog='Speedtracker',
        description='A program for tracking internet download speeds.'
        )
    parser.set_defaults(handler = quick_test)
    subparsers = parser.add_subparsers()

    parser_quick = subparsers.add_parser("quick")
    parser_quick.set_defaults(handler = quick_test)

    parser_test = subparsers.add_parser("test")
    parser_test.add_argument("--silent", "-q", action = "store_true")
    parser_test_size_group = parser_test.add_mutually_exclusive_group()
    parser_test_size_group.add_argument("--small", "-s", action = "store_const", const = "small", dest = "size")
    parser_test_size_group.add_argument("--medium", "-m", action = "store_const", const = "medium", dest = "size")
    parser_test_size_group.add_argument("--large", "-l", action = "store_const", const = "large", dest = "size")
    parser_test.set_defaults(size = "medium")
    parser_test.add_argument("--number", "-n", type = int, nargs = 1, default = [3])
    parser_test.add_argument("logfile", type = str, nargs = '?', default = None)
    parser_test.set_defaults(handler = test)

    args = parser.parse_args()
    args.handler(args)

if __name__ == "__main__":
    main()
