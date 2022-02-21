from pydub import AudioSegment
import glob
import numpy

wav_files = sorted(glob.glob('data/*.wav'))

print(wav_files)

# defining arrays
sound_array = []
sound_length_array = []

for wav_file in wav_files:	
	# load file as audiosegment object
	sound = AudioSegment.from_wav(wav_file)
	# append to array
	sound_array.append(sound)
	sound_length_array.append(sound.duration_seconds)
	# test printing attributes
#print(wav_file, sound.duration_seconds, sound.frame_rate, sound.sample_width)

# collect maximum duration of a sound
max_duration = numpy.max(sound_length_array)
#print(max_duration)

# append silence to make all sounds the same length
for index in range(len(sound_array)):
	silence_to_append = max_duration - sound_array[index].duration_seconds
	#print(sound_array[index].duration_seconds * 1000, silence_to_append, max_duration, silence_to_append + sound_array[index].duration_seconds)
	sound_array[index] = sound_array[index] + AudioSegment.silent(duration=silence_to_append*1000, frame_rate=44100)

#iterate and append audio to final clip
final_clip = sound_array[0]
for index in range(1,len(sound_array)):
	#print(sound_array[index].duration_seconds)
	final_clip = final_clip + sound_array[index]

#print(final_clip.duration_seconds)

# write result
final_clip.export("result.wav", format="wav")
