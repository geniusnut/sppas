## AudioRoamer

`AudioRoamer` allows to play audio files, to display general information about
a digitalized audio-PCM file and to manipulate the file.

Pulse-code modulation (PCM) is a method used to digitally represent sampled 
analog signals. In a PCM stream, the amplitude of the analog signal is sampled 
regularly at uniform intervals. A PCM stream has two basic properties that 
determine the stream's fidelity to the original analog signal: 

1. the sampling rate, which is the number of times per second that samples are taken; 
2. the bit depth, which determines the number of possible digital values that can be used to represent each sample.

Common sampling frequencies are 48 kHz as used with DVD format videos, or 
44.1 kHz as used in Compact discs. Common sample depths are 8, 16 or 24 
bits per sample. 16 is the most frequent one: this allow values to range from
-32768 to 32767.

Support for multichannel audio depends on file format and relies on 
interweaving or synchronization of streams.

![AudioRoamer: play and manage audio files](./etc/screenshots/AudioRoamer.png)


When an audio file is checked in the list of files, a new page is opened in
the notebook. The main information about the audio file are then displayed
in the panel at the middle and a player is displayed at bottom. The audio
file is not loaded in memory, so event very long audio files can be 
displayed.
At the top of the page, a button "Want more?" can be clicked: the audio 
file will then be fully read and analyzed, then a new window will be 
opened to display detailed information. It will also allow to change some
properties of the audio file, extract a channel, etc. 



### Properties of the audio file

The main properties of any audio file is displayed. SPPAS can open audio files
of type:

1. Waveform Audio File Format (WAVE), a Microsoft and IBM audio file format standard;
2. Audio Interchange File Format (AIFF), an audio file format standard developped by Apple Inc;
3. Au file format, a simple audio file format introduced by Sun Microsystems.

The following information are extracted or deducted of the header of the 
audio file:

- the duration given in seconds with a maximum of 3 digits;
- the frame rate given in Hz;
- the sample width in bits (one of 8, 16, 24 or 32);
- the number of channels.


A color code is used to indicate if the file is compatible with SPPAS automatic
annotations:

- Green color indicates that the value is perfectly matching the expectations;
- Orange color indicates that the value is not the expected one but automatic annotations will be able to convert it to the right one;
- Red color indicates that none of the automatic annotations will work with the given value. The file must be modified.



### Playing audio files


The following shortcuts can be used:

- TAB: Play
- ESC: Stop
- F6: Rewind
- F7: Pause
- F8: Next



### Want more?

`AudioRoamer` allows to display a large set of information for each channel.
For a large file, it can take a while to estimate such information... 
For example, an mono-audio file of 243 seconds (21.5Mb) is loaded in 35 seconds.
**So be patient! It's worth it!**

![AudioRoamer if you want more](./etc/screenshots/AudioRoamer-more.png)

At the bottom of the window, it is possible to click on buttons to:

1. Save the channel currently displayed;
2. Save a portion (from...to...) of the channel;
3. Save the displayed information in a text file;
4. Close the window.

There are 3 main columns of information, related to amplitude, clipping and 
volume.


#### Amplitude

The amplitude is a variable characterizing the sinusoidal oscillation of the
digital-audio recording. It gives the deflection of a physical quantity from 
its neutral position (zero point) up to a positive or negative value.
With sound waves, it is the extent to which air particles are displaced, and 
this amplitude of sound or sound amplitude is experienced as the loudness of 
sound. The loudness perception of a sound is determined by the amplitude of 
the sound waves − the higher the amplitude, the louder the sound or the noise.

The first column of `AudioRoamer` Data Manager gives amplitude values of each 
channel of the PCM file:

- Number of frames: the number of samples, i.e. the number of amplitude values;
- Min/Max values: minimum and maximum amplitude values in the channel;
- Zero crossings

The 5 information below can be modified and modifications can be saved 
separatly for each channel:

- Frame rate: the sampling frequency observed in the channel included in a list of possible values. If it is modified, the color is changed.
- Samp. width: the bit depth observed in the channel included in a list of possible values. If it is modified, the color is changed.
- Multiply values by: all samples in the original channel are multiplied by the floating-point value factor. Sample values are truncated in case of overflow.
- Add bias value: a bias value is added to each sample. Sample values wrap around in case of overflow.
- Remove offset value: the average over all values is deduced to each sample. Sample values wrap around in case of overflow.


#### Clipping

The second column displays the clipping rates of the sample values given a 
factor. It will consider that all values outside the interval are clipped.
The clipping rate is given as a percentage related to the total number of
values.


#### Volume

##### RMS:

Volume is estimated from root-mean-square (RMS) of the samples, i.e. 
sqrt(sum(S_i^2)/n). This is a measure of the power in an audio signal.
Between parenthesis, the volume in dB is estimated as: 
10.log10(rms/ref), where ref is a reference factor (energy quantity) 
ref = 1 ≡ 0 dB (power).

*Illustration:*
The level of −3 dB is equivalent to 50% (factor = 0.5) and the level of
−6 dB is equivalent to 25% (factor = 1/4 = 0.25) of the initial power.
For example, a RMS value of 350 gives a pover value equal to 25.45 dB compared
to a RMS value of 700 that gives a power value of 28.45 dB.

##### Automatic detection of silences:

Finally, the result of an automatic detection of silences is given. Of course,
this information is given for information only. It is estimated with default
parameters which should be adapted. 
