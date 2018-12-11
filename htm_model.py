from __future__ import print_function

from datetime import timedelta, datetime

from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.algorithms import anomaly_likelihood
import nupic_anomaly_output
from nupic.data.inference_shifter import InferenceShifter
from util import make_row
from tqdm import tqdm

true = True
null = None
false = False

# canned params provided by nupic
model_params3 = {
    "aggregationInfo": {
        "seconds": 0,
        "fields": [],
        "months": 0,
        "days": 0,
        "years": 0,
        "hours": 0,
        "microseconds": 0,
        "weeks": 0,
        "minutes": 0,
        "milliseconds": 0
    },
    "model": "HTMPrediction",
    "version": 1,
    "predictAheadTime": null,
    "modelParams": {
        "inferenceType": "TemporalAnomaly",
        "sensorParams": {
            "encoders": {
                "c0_timeOfDay": {
                    "type": "DateEncoder",
                    "timeOfDay": [
                        21,
                        9.49
                    ],
                    "fieldname": "datetime",
                    "name": "c0"
                },
                "c0_dayOfWeek": null,
                "c0_weekend": null,
                "c1": {
                    "name": "c1",
                    "fieldname": "measured_flow",
                    "resolution": 1.538,
                    "type": "RandomDistributedScalarEncoder"
                },
                "_classifierInput": {
                    "classifierOnly": True,
                    "type": "RandomDistributedScalarEncoder",
                    "resolution": 1.538,
                    "fieldname": "measured_flow",
                    "name": "_classifierInput"
                },
            },
            "sensorAutoReset": null,
            "verbosity": 0
        },
        "spEnable": true,
        "spParams": {
            "spatialImp": "cpp",
            "potentialPct": 0.8,
            "columnCount": 2048,
            "globalInhibition": 1,
            "inputWidth": 0,
            "boostStrength": 0.0,
            "numActiveColumnsPerInhArea": 40,
            "seed": 1956,
            "spVerbosity": 0,
            "synPermActiveInc": 0.003,
            "synPermConnected": 0.2,
            "synPermInactiveDec": 0.0005
        },
        "trainSPNetOnlyIfRequested": false,
        "tmEnable": true,
        "tmParams": {
            "activationThreshold": 20,
            "cellsPerColumn": 32,
            "columnCount": 2048,
            "globalDecay": 0.0,
            "initialPerm": 0.24,
            "inputWidth": 2048,
            "maxAge": 0,
            "maxSegmentsPerCell": 128,
            "maxSynapsesPerSegment": 128,
            "minThreshold": 13,
            "newSynapseCount": 31,
            "outputType": "normal",
            "permanenceDec": 0.008,
            "permanenceInc": 0.04,
            "predictedSegmentDecrement": 0.001,
            "seed": 1960,
            "temporalImp": "tm_cpp",
            "verbosity": 0
        },
        "clEnable": True,
        "clParams": {
            "alpha": 0.035828933612157998,
            "regionName": "SDRClassifierRegion",
            "steps": "1",
            "verbosity": 0
        },
        "anomalyParams": {
            "anomalyCacheRecords": null,
            "autoDetectThreshold": null,
            "autoDetectWaitRecords": 5030
        }
    }
}

model_params2 = {
    "aggregationInfo": {"seconds": 0, "fields": [], "months": 0, "days": 0, "years": 0, "hours": 0, "microseconds": 0,
                        "weeks": 0, "minutes": 0, "milliseconds": 0},
    "model": "HTMPrediction",
    "version": 1,
    "predictAheadTime": null,
    "modelParams": {"sensorParams": {"verbosity": 0,
                                     "encoders": {
                                         "_classifierInput": {
                                             "classifierOnly": True,
                                             "type": "RandomDistributedScalarEncoder",
                                             "resolution": 81,
                                             "fieldname": "measured_flow",
                                             "name": "_classifierInput"
                                         },
                                         "measured_flow": {
                                             "type": "RandomDistributedScalarEncoder",
                                             "resolution": 81,
                                             "fieldname": "measured_flow",
                                             "name": "measured_flow"
                                         },
                                         "datetime_timeOfDay": {
                                             "type": "DateEncoder",
                                             "timeOfDay": [67, 11.105978995691185],
                                             "fieldname": "datetime",
                                             "name": "datetime_timeOfDay"
                                         },

                                         "datetime_weekend": {
                                             "weekend": [67, 14.275074222333311],
                                             "fieldname": "datetime", "name": "datetime_weekend",
                                             "type": "DateEncoder"
                                         },
                                         "datetime_dayOfWeek": {
                                             "dayOfWeek": [67, 14.38253450889498],
                                             "type": "DateEncoder",
                                             "fieldname": "datetime",
                                             "name": "datetime_dayOfWeek"
                                         }},
                                     "sensorAutoReset": null},
                    "anomalyParams": {"anomalyCacheRecords": null,
                                      "autoDetectThreshold": null,
                                      "autoDetectWaitRecords": null},
                    "spParams": {"columnCount": 2048,
                                 "spVerbosity": 0,
                                 "spatialImp": "cpp",
                                 "inputWidth": 0,
                                 "synPermInactiveDec": 0.07337673496672821,
                                 "synPermConnected": 0.20011487081872253,
                                 "synPermActiveInc": 0.07872845361331532,
                                 "seed": 1956,
                                 "numActiveColumnsPerInhArea": 36,
                                 "boostStrength": 0.032909656895874155,
                                 "globalInhibition": 1,
                                 "potentialPct": 0.6634885586687228},
                    "trainSPNetOnlyIfRequested": false,
                    "clParams": {
                        "alpha": 0.02269254902966883,
                        "verbosity": 0,
                        "steps": "1",
                        'implementation': 'cpp',
                        "regionName": "SDRClassifierRegion"
                    },
                    "tmParams": {
                        "columnCount": 2048,
                        "activationThreshold": 8,
                        "pamLength": 7,
                        "cellsPerColumn": 18,
                        "permanenceInc": 0.06129927857024438,
                        "minThreshold": 7,
                        "verbosity": 0,
                        "maxSynapsesPerSegment": 60,
                        "outputType": "normal",
                        "globalDecay": 0.0,
                        "initialPerm": 0.24605421437600467,
                        "permanenceDec": 0.13494965672770592,
                        "seed": 1960,
                        "maxAge": 0,
                        "newSynapseCount": 28,
                        "maxSegmentsPerCell": 58,
                        "temporalImp": "cpp",
                        "inputWidth": 2048},
                    "tmEnable": true,
                    "clEnable": true,
                    "spEnable": true,
                    "inferenceType": "TemporalAnomaly"
                    }
}

model_params1 = {
    'aggregationInfo': {'days': 0,
                        'fields': [],
                        'hours': 0,
                        'microseconds': 0,
                        'milliseconds': 0,
                        'minutes': 0,
                        'months': 0,
                        'seconds': 0,
                        'weeks': 0,
                        'years': 0},
    'model': 'HTMPrediction',
    'modelParams': {
        'anomalyParams': {'anomalyCacheRecords': None,
                          'autoDetectThreshold': None,
                          'autoDetectWaitRecords': 5030},
        'clEnable': True,
        'clParams': {'alpha': 0.01962508905154251,
                     'verbosity': 0,
                     'regionName': 'SDRClassifierRegion',
                     'implementation': 'cpp',
                     'steps': '1'},
        'inferenceType': 'TemporalAnomaly',
        'sensorParams': {'encoders': {
            'datetime_weekend': {
                'fieldname': 'datetime',
                'name': 'datetime_weekend',
                'weekend': (37, 1),
                'type': 'DateEncoder'
            }, 'datetime_timeOfDay': {
                'fieldname': 'datetime',
                'name': 'datetime_timeOfDay',
                'type': 'DateEncoder',
                'timeOfDay': (37, 6.09)
            }, 'datetime_dayOfWeek': {
                'fieldname': 'datetime',
                'name': 'datetime_dayOfWeek',
                'type': 'DateEncoder',
                'dayOfWeek': (37, 9.49)
            }

        },
            'sensorAutoReset': None,
            'verbosity': 0},
        'spEnable': True,
        'spParams': {
            'spVerbosity': 0,
            'spatialImp': 'cpp',
            'globalInhibition': 1,
            'columnCount': 2048,
            'inputWidth': 0,
            'numActiveColumnsPerInhArea': 40,
            'seed': 1956,

            'potentialPct': 0.8,
            'synPermConnected': 0.1,
            'synPermActiveInc': 0.003,
            'synPermInactiveDec': 0.08568228006654939,
            # 'maxBoost': 1.0,
        },

        'tmEnable': True,
        'tmParams': {
            'verbosity': 0,
            'columnCount': 2048,
            'cellsPerColumn': 32,
            'inputWidth': 2048,
            'seed': 1960,
            'temporalImp': 'cpp',
            'newSynapseCount': 20,
            'maxSynapsesPerSegment': 32,
            'maxSegmentsPerCell': 128,
            'initialPerm': 0.21,
            'permanenceInc': 0.1,
            'permanenceDec': 0.1,
            'globalDecay': 0.0,
            'maxAge': 0,
            'minThreshold': 12,
            'activationThreshold': 12,
            'outputType': 'normal',
            'pamLength': 1,
        },
        'trainSPNetOnlyIfRequested': False
    },
    'predictAheadTime': None,
    'version': 1
}


def get_sensor_encoder(name, maxval=False, buckets=40, max_vehicles=200):
    if maxval:
        max_vehicles = maxval

    resolution = max(0.001, (max_vehicles - 1) / buckets)
    return {
        'fieldname': name,
        'name': name,
        'resolution': resolution,
        'w': 21,
        'type': 'RandomDistributedScalarEncoder'
    }


threshold = 0.99995


def run_model(coll, data, location, si, ds, count):
    name = 'measured_flow'
    MODEL_PARAMS = model_params3
    # MODEL_PARAMS['modelParams']['sensorParams']['encoders'][name] = input_encoder
    shifter = InferenceShifter()
    # classifier_encoder = {k: v for k, v in input_encoder.items()}
    # classifier_encoder['classifierOnly'] = True
    # classifier_encoder['name'] = '_classifierInput'
    # MODEL_PARAMS['modelParams']['sensorParams']['encoders']['_classifierInput'] = classifier_encoder
    model = ModelFactory.create(MODEL_PARAMS)
    model.enableInference({'predictedField': 'measured_flow'})
    readings_per_week = 288 * 7
    if ds == 'sm':
        # get approx readings per week
        sdate = datetime(2012, 3, 1)
        readings_per_week = coll.database['scats_sm_small'].find({
            "site_no": location['site_no'],
            "strategic_input": int(si),
            "datetime": {
                "$gte": sdate,
                "$lte": sdate + timedelta(days=7)
            }
        }).count()
    print("Readings per week for {}: {}".format(ds, readings_per_week))
    anomaly_likelihood_helper = anomaly_likelihood.AnomalyLikelihood(historicWindowSize=readings_per_week)

    # output = nupic_anomaly_output.NuPICPlotOutput(location['site_no'])
    prog = tqdm(total=count, desc="HTM")
    for row in data:
        to_process = make_row(row, location, ds, si)

        result = model.run(to_process)
        result = shifter.shift(result)
        raw_anomaly_score = result.inferences['anomalyScore']
        likelihood = anomaly_likelihood_helper.anomalyProbability(to_process['measured_flow'], raw_anomaly_score,
                                                                  to_process['datetime'])
        pred = result.inferences["multiStepBestPredictions"][1]
        # output.write(to_process['datetime'], to_process['measured_flow'], pred, raw_anomaly_score)
        # print("observed:", last, "predicted:", pred)
        # last = to_process['measured_flow']
        # print("raw anomaly:", raw_anomaly_score, "likelihood:", likelihood)
        if likelihood >= threshold:
            try:
                doc = {'site_no': location['site_no'],
                       'strategic_input': si,
                       'algorithm': 'HTM',
                       'datetime': row['datetime'],
                       'ds': ds,
                       'other': {'likelihood': float(likelihood), 'score': float(raw_anomaly_score)}}
                # print(doc)
                coll.insert_one(doc)
            except Exception as e:
                print(e)
        prog.update()
