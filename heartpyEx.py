import heartpy as hp

data = hp.get_data('data.csv')
working_data, measures = hp.process(data, 100.0, calc_freq=True, freq_method='fft')
#hp.plotter(working_data, measures)

"""
Time domain:

    - beats per minute, BPM
    - interbeat interval, IBI
    - standard deviation if intervals between adjacent beats, SDNN
    - standard deviation of successive differences between adjacent R-R intervals, SDSD
    - root mean square of successive differences between adjacend R-R intervals, RMSSD
    - proportion of differences between R-R intervals greater than 20ms, 50ms, pNN20, pNN50
    - median absolute deviation, MAD
    - Poincare analysis (SD1, SD2, S, SD1/SD1)
    - Poincare plotting
"""
for measure in measures.keys():
    print('%s: %f' %(measure, measures[measure]))

def linear_HRV_Classification_Tree_Algorithm(measures):
    """ Classification tree for real-life stress detection
        using linear Heart Rate Variability analysis.

        Stress detection sensitivity rate: 83.33%
                         specificity rate: 90.48%
                         Accuracy: 70%
    """
    
    if (measures['lf']<899.58 and measures['pnn50']>.9873) or (measures['lf']<277.28 and measures['pnn50']<.9873):
        return 'stressful state'
    if measures['lf']>899.58 or (measures['lf']>277.28 and measures['pnn50']<0.9783):
        return 'restful state'
    return 'uncertain state'

print(linear_HRV_Classification_Tree_Algorithm(measures))
