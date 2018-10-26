import subprocess as sp

tss = [('3001', ['6', '121', '122', '123', '124', '125']),
       ('3043', ['144', '145', '146', '147', '148', '344', '345']),
       ('115', ['1', '2', '3', '4', '5']),
       ('100', ['39', '38', '41', '40', '42', '209', '210', '217']),
       ('221', ['166', '167', '168', '169', '170'])]

for ts, sis in tss:
    for si in sis:
        for ds in ['vs', 'sm']:
            for method in ['htm', 's-h-esd', 's-esd']:
                sp.check_output(['qsub', '-cwd', '-pe', 'threaded', '8', '-q', '8g.q',
                                 '-N', '{}-{}-{}-{}'.format(*[ts, si, ds, method]), '-o', 'output_$JOB_NAME.log',
                                 '-e', 'error_$JOBNAME.log', '-v',
                                 'ts={},ds={},method={},si={}'.format(ts, ds, method, si),
                                 'job_runner.csh'])
