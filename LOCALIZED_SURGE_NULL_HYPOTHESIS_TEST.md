# Localized Surge Analysis: Null Hypothesis Test

## Critical Question: Is 4.3% Better Than Random?

**SHORT ANSWER: NO** ❌

The corrected 4.30% localized surge rate is **NOT statistically distinguishable from random false positives** expected under FDR correction (α = 0.05).

## Statistical Test Results

### Binomial Test
- **Null hypothesis (H₀)**: True rate = 5.0% (random false positives from FDR)
- **Alternative (H₁)**: True rate ≠ 5.0% (real signal)
- **Observed**: 107/2,488 phrases = 4.30%
- **Expected**: 124.4 phrases = 5.00%
- **p-value**: 0.118 (NOT significant)
- **Conclusion**: Cannot reject null hypothesis

### 95% Confidence Interval
- **Observed rate CI**: [3.54%, 5.10%]
- **Does CI include 5%?** YES ✓
- **Interpretation**: True rate could plausibly be exactly 5% (pure noise)

### Effect Size
- **Absolute difference**: -0.70 percentage points (107 vs 124 phrases)
- **Relative difference**: -14% lower than expected
- **Direction**: Actually LOWER than expected by chance (though not significantly)

## What This Means

### 1. **Localized Surges May Be Entirely False Positives**
The 107 "significant" phrases could all be Type I errors (false positives) from:
- FDR allowing 5% false discovery rate
- Expected false positives: 124 phrases
- Observed: 107 phrases (within statistical noise)

### 2. **No Evidence of Real Localized Surge Phenomenon**
Unlike full-phrase Mann-Kendall (1.81% - significantly below 5%), the localized surge rate:
- Is consistent with pure noise
- Shows no signal above random fluctuation
- Cannot be distinguished from FDR false positives

### 3. **Comparison Across Analysis Types**

| Analysis | Rate | Expected Random | Significantly Different? | Interpretation |
|----------|------|-----------------|-------------------------|----------------|
| **Full-phrase Mann-Kendall** | 1.81% | 5.00% | YES (p < 0.001) | **REAL SIGNAL** ✓ |
| **Full-phrase Linear Reg** | 0.04% | 5.00% | YES (p < 0.001) | **REAL SIGNAL** ✓ |
| **Localized Surge (corrected)** | 4.30% | 5.00% | NO (p = 0.118) | **NO SIGNAL** ❌ |
| **Localized Surge (old)** | 17.6% | 5.00% | YES (p < 0.001) | Invalid (bad stats) |

### 4. **Why Full-Phrase Shows Signal But Localized Doesn't**

**Full-phrase Mann-Kendall (1.81%)**:
- Significantly BELOW 5% false positive rate
- Strong evidence of real trend detection
- Conservative estimate of true phenomenon

**Localized surge (4.30%)**:
- NOT significantly different from 5% 
- Could be entirely false positives
- No evidence beyond random chance

## Implications for Research Conclusions

### Original (Flawed) Claim
> "BUR surges are primarily localized (17.6%), not full-phrase (1.81%)"
- **Status**: INVALID (bad statistics)

### Corrected but Naive Interpretation
> "Localized surges (4.30%) are more common than full-phrase (1.81%)"
- **Status**: MISLEADING (doesn't account for null expectation)

### **Correct Scientific Conclusion**
> "Full-phrase BUR trends are rare but REAL (1.81% vs 5% expected). Localized surges cannot be distinguished from random noise (4.30% vs 5% expected). BUR patterns are predominantly STABLE within phrases, with occasional weak full-phrase trends."

## Statistical Power Analysis

### Why Might We Fail to Detect Real Signal?

1. **Multiple testing penalty is severe**:
   - 43,532 tests → very conservative FDR threshold
   - Real weak signals may not survive correction

2. **Effect sizes are tiny**:
   - Mean tau = -0.025 (nearly zero)
   - Even "significant" windows have trivial trends

3. **Overlapping windows create noise**:
   - 75-88% overlap between adjacent windows
   - Pseudo-replication inflates noise
   - Real signals diluted by redundant tests

4. **Period=4 assumption may be wrong**:
   - Seasonal Mann-Kendall assumes 4-beat cycles
   - If wrong, adds noise instead of removing it
   - No validation of periodicity assumption

## Alternative Explanations for 107 "Significant" Phrases

### Hypothesis 1: Pure False Positives (Most Likely)
- **Evidence**: 
  - Rate (4.30%) ≈ expected FDR rate (5.00%)
  - p = 0.118 (not significant)
  - CI includes 5%
- **Conclusion**: All 107 could be Type I errors

### Hypothesis 2: Mix of Real + False Positives
- **Evidence**:
  - Slightly below 5% (though not significantly)
  - Some windows show decent tau values
- **Problem**: Cannot identify which are real vs false
- **Conclusion**: Even if some are real, signal is too weak to detect

### Hypothesis 3: Conservative FDR Missing Real Signals
- **Evidence**: 
  - FDR is conservative by design
  - Mean tau = -0.025 suggests weak real trends
- **Problem**: If real, why not detected in full-phrase analysis?
- **Conclusion**: Unlikely - full-phrase should be more powerful

## Methodological Issues Remaining

### 1. Window Overlap Violates Independence
- Adjacent windows share 75-88% of data
- FDR assumes independent tests
- True false positive rate may be higher than 5%

### 2. Post-hoc Filtering by Tau
- Applied min_tau=0.4 AFTER FDR correction
- Changes effective alpha
- Should be part of hypothesis specification

### 3. Unjustified Periodicity Assumption
- period=4 not validated
- Could increase noise if wrong
- Should test for periodicity first

### 4. Mixed Test Types
- Seasonal MK for large windows
- Modified MK for small windows
- Different tests have different properties
- Comparing p-values across types is questionable

## Recommendations

### For Manuscript

**DO NOT CLAIM**:
- ❌ "Localized surges are common (4.30%)"
- ❌ "Localized surges more common than full-phrase"
- ❌ "BUR dynamism is primarily localized"

**DO REPORT**:
- ✓ "No evidence of localized surges beyond random noise"
- ✓ "4.30% rate consistent with FDR false positives (p = 0.118)"
- ✓ "Full-phrase trends (1.81%) represent real but rare phenomenon"
- ✓ "BUR patterns are predominantly stable within phrases"

### For Future Analysis

1. **Use non-overlapping windows** to satisfy independence
2. **Validate period=4 assumption** (ACF, spectral analysis)
3. **Use single test type** (seasonal OR modified, not both)
4. **Specify tau threshold a priori** (not post-hoc)
5. **Consider permutation tests** to empirically estimate null
6. **Focus on full-phrase analysis** (cleaner, more powerful)

## Final Verdict

| Question | Answer |
|----------|--------|
| Is 4.3% significant? | YES (survives FDR correction) |
| Is 4.3% better than random? | **NO** (p = 0.118) |
| Do localized surges exist? | **UNCLEAR** (cannot distinguish from noise) |
| Should we report localized surges? | **NO** (no evidence beyond false positives) |
| What should we conclude? | **BUR is predominantly stable** |

## Date of Analysis
October 3, 2025

## Statistical Details
- Test: Two-tailed binomial test
- Observed: 107/2,488 = 4.30%
- Expected under H₀: 124.4/2,488 = 5.00%
- p-value: 0.118
- 95% CI: [3.54%, 5.10%]
- Conclusion: Cannot reject null hypothesis of random false positives
