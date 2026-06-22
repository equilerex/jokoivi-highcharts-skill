Speech
===

There are two types of tracks available in the Highcharts sonification module: Instrument tracks and Speech tracks. A speech track is a track that plays speech announcements using speech synthesis.

Speech tracks have parameters that can be mapped to, just like instrument tracks, including `volume`, `rate` and `pitch`. For a full list of available options for speech tracks, see defaultSpeechOptions.

Basic Speech Tracks
-------------------

To define a speech track, set the track `type` to `"speech"`:

```js
series: [{
    data: [1, 2, 3, 4, 5],
    sonification: {
        tracks: [{
            // This is an instrument track
            instrument: 'flute',
            mapping: {
                volume: 0.8
            }
        }, {
            // This is a speech track
            type: 'speech',
            mapping: {
                volume: 0.4,
                text: 'Hello world'
            }
        }]
    }
}]
```

Speech Mapping
--------------

The text mapping parameter determines what is being spoken. It can either be a [format string](./chart-concepts/labels-and-string-formatting#format-strings) or a function.

The below demo illustrates using a format string to map the speech to announce Y-values. It also maps the speech pitch to Y-values, meaning the voice speaks at a higher pitch at higher values, and lower at lower values.

<iframe style="width: 100%; height: 490px; border: none;" src="" allow="fullscreen"></iframe>


Next Steps
----------
Often with speech tracks we don't want them to play all the time. Next up is looking at [conditional tracks](./sonification/conditional-tracks), a powerful tool when building sonifications.
