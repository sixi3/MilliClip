#!/usr/bin/env python3
"""Illustrative sample-size simulation for MilliClip A/B tests (stdlib + numpy only).

EVERYTHING HERE IS ASSUMPTION-DRIVEN. Nothing is measured from real channels.
Replace the assumed spreads with estimates from your own posts once ~30-50
exist, then re-run.

Model 1 (noisy): per-post views ~ LogNormal(mu, sigma); arm B's MEDIAN is r times
  arm A's (shift in mu by ln r). sigma is the log-sd (0.8 / 1.2 / 1.6).
Model 2 (low-variance proxy): per-post average % viewed ~ Beta with mean m and
  concentration kappa (sd = sqrt(m(1-m)/(kappa+1))); arm B adds +delta points.

Tests (two-sided, alpha=0.05, equal posts per arm, unit = one distinct clip):
  - log-t   : Welch t statistic on log(views)       (best case for log-normal data)
  - raw-t   : Welch t statistic on raw views        (the naive "compare mean views")
  - prop-t  : Welch t statistic on the proxy
Critical values are calibrated by simulating the null at each n, so small-n
t-approximation error does not bias power.

Usage: python3 scripts/sample_size_sim.py [--reps 3000] [--seed 7]
"""
import argparse
import numpy as np

N_GRID = [10, 15, 20, 30, 40, 60, 80, 100, 150, 200, 300, 500, 800, 1200, 2000, 4000]


def welch_t(a, b):
    """Row-wise Welch t statistic for arrays shaped (reps, n)."""
    ma, mb = a.mean(1), b.mean(1)
    va, vb = a.var(1, ddof=1), b.var(1, ddof=1)
    return (mb - ma) / np.sqrt(va / a.shape[1] + vb / b.shape[1] + 1e-300)


def beta_draw(rng, mean, kappa, size):
    return rng.beta(mean * kappa, (1 - mean) * kappa, size=size)


def power_curve(gen_null, gen_alt, test_stat, reps, rng):
    """Return {n: power}, calibrating the critical value at each n from the null."""
    out = {}
    for n in N_GRID:
        a, b = gen_null(rng, n, reps)
        crit = np.quantile(np.abs(test_stat(a, b)), 0.95)
        a, b = gen_alt(rng, n, reps)
        out[n] = float((np.abs(test_stat(a, b)) > crit).mean())
    return out


def n_for_power(curve, target=0.8):
    prev = None
    for n in N_GRID:
        if curve[n] >= target:
            if prev is None:
                return n
            n0, p0 = prev
            return int(np.ceil(n0 + (target - p0) * (n - n0) / (curve[n] - p0)))
        prev = (n, curve[n])
    return None  # not reached within grid


def lognormal_gens(sigma, ratio):
    def null(rng, n, reps):
        return (rng.normal(0, sigma, (reps, n)), rng.normal(0, sigma, (reps, n)))

    def alt(rng, n, reps):
        return (rng.normal(0, sigma, (reps, n)),
                rng.normal(np.log(ratio), sigma, (reps, n)))
    return null, alt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    fmt = lambda v: ">%d" % N_GRID[-1] if v is None else str(v)

    print("== Model 1: log-normal views; posts PER ARM for 80%% power, alpha=0.05 (reps=%d) ==" % args.reps)
    print("%-8s %-6s %-10s %-10s" % ("sigma", "ratio", "log-t", "raw-t(naive)"))
    for sigma in (0.8, 1.2, 1.6):
        for ratio in (1.5, 2.0):
            null_l, alt_l = lognormal_gens(sigma, ratio)
            c_log = power_curve(null_l, alt_l, welch_t, args.reps, rng)

            def exp_gen(g):
                def f(rng_, n, reps):
                    a, b = g(rng_, n, reps)
                    return np.exp(a), np.exp(b)
                return f
            c_raw = power_curve(exp_gen(null_l), exp_gen(alt_l), welch_t, args.reps, rng)
            print("%-8s %-6s %-10s %-10s" % (sigma, ratio, fmt(n_for_power(c_log)), fmt(n_for_power(c_raw))))

    print("\n== Model 2: avg % viewed ~ Beta(mean=0.55, kappa); posts PER ARM for 80% power ==")
    print("%-8s %-8s %-10s" % ("kappa", "sd(pts)", "delta=+5pts / +10pts"))
    m = 0.55
    for kappa in (10, 20, 40):
        sd = (m * (1 - m) / (kappa + 1)) ** 0.5 * 100
        res = []
        for delta in (0.05, 0.10):
            def null(rng_, n, reps, kappa=kappa):
                return beta_draw(rng_, m, kappa, (reps, n)), beta_draw(rng_, m, kappa, (reps, n))

            def alt(rng_, n, reps, kappa=kappa, delta=delta):
                return beta_draw(rng_, m, kappa, (reps, n)), beta_draw(rng_, m + delta, kappa, (reps, n))
            res.append(fmt(n_for_power(power_curve(null, alt, welch_t, args.reps, rng))))
        print("%-8d %-8.1f %s / %s" % (kappa, sd, res[0], res[1]))

    print("\n== False-positive illustration: A/A (no true difference), 20 posts/arm, sigma=1.6 ==")
    null_l, _ = lognormal_gens(1.6, 1.0)
    a, b = null_l(rng, 20, 20000)
    a, b = np.exp(a), np.exp(b)
    # naive rule: 'B wins' if mean raw views of B exceeds A by >=20%
    naive = ((b.mean(1) / a.mean(1)) >= 1.2).mean()
    # rule: median-of-logs differ by >= ln(1.2)
    med = ((np.median(np.log(b), 1) - np.median(np.log(a), 1)) >= np.log(1.2)).mean()
    print("P(naive 'mean views +20%%' declares B the winner | no true effect) = %.2f" % naive)
    print("P(median-of-logs +20%% declares B the winner | no true effect)  = %.2f" % med)


if __name__ == "__main__":
    main()
