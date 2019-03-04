import argparse
import wer

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=reference_string, hyp=hypothesis_string)
#


def WER_compute(rline, hline, size):
    """Computes the word error rate between two lines."""
    t, e, d, i, s = wer.string_edit_distance(ref=rline.split(), hyp=hline.split())
    print(t, e, d, i, s)
    tokens = 0
    for lines in range(size):
        tokens += t
    return (d + i + s)/tokens


def SER_count(rline, hline):
    """Computes the total incorrect sentences between two transcriptions."""
    err_sent = 0
    _, e, _, _, _ = wer.string_edit_distance(ref=rline.split(), hyp=hline.split())
    if e > 0:
        err_sent = 1
    return err_sent


def score(ref_trn=None, hyp_trn=None):

    with open(ref_trn) as f:
        size = sum(1 for _ in f)

    WER = sum(WER_compute(rline, hline, size) for rline, hline in zip(open(ref_trn), open(hyp_trn)))
    SER = sum(SER_count(rline, hline) for rline, hline in zip(open(ref_trn), open(hyp_trn)))/size
    return WER, SER


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    WER, SER = score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)
    print("WER:", (WER * 100), "%", "SER:", (SER*100), "%")
