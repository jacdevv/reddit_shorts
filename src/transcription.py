def convert_words_to_dict(data, words_per_group=2):
    result = {}
    words = [word for segment in data['segments'] for word in segment['words']]
    for i in range(0, len(words), words_per_group):
        group = words[i:i+words_per_group]
        start_time = group[0]['start']
        end_time = group[-1]['end']
        content = ' '.join(word['text'] for word in group)
        result[start_time] = (content, end_time)
    return result