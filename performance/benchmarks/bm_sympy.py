import perf
from six.moves import xrange

from sympy import expand, symbols, integrate, tan, summation
from sympy.core.cache import clear_cache


def bench_expand():
    x, y, z = symbols('x y z')
    expand((1 + x + y + z) ** 20)


def bench_integrate():
    x, y = symbols('x y')
    f = (1 / tan(x)) ** 10
    return integrate(f, x)


def bench_sum():
    x, i = symbols('x i')
    summation(x ** i / i, (i, 1, 400))


def bench_str():
    x, y, z = symbols('x y z')
    str(expand((x + 2 * y + 3 * z) ** 30))


def bench_sympy(loops, func):
    timer = perf.perf_counter
    dt = 0

    for _ in xrange(loops):
        # Don't benchmark clear_cache(), exclude it of the benchmark
        clear_cache()

        t0 = timer()
        func()
        dt += (timer() - t0)

    return dt


def prepare_cmd(runner, cmd):
    cmd.append(runner.args.benchmark)


if __name__ == "__main__":
    runner = perf.Runner(name='sympy')
    runner.metadata['description'] = "SymPy benchmark"
    runner.prepare_subprocess_args = prepare_cmd
    runner.argparser.add_argument("benchmark",
                                  choices=("expand", "integrate", "sum",
                                           "str"))

    args = runner.parse_args()
    bench = args.benchmark

    runner.name += "_%s" % bench
    func = globals()['bench_' + bench]
    runner.bench_sample_func(bench_sympy, func)
