from wordcloud import WordCloud
import matplotlib.pyplot as plt


#implementation instruction -  plot_word_cloud(create_word_cloud(quotes_df))

"""
takes a df in which the 2nd column is the text(quotes_df or reviews_df) and returns a wordcloud object
"""
def create_word_cloud(df):
	#createing text object from text column in df 
	text_df = df['content']
	text_series = text_df.squeeze()
	text = " ".join(text_series)


	#removing suprficial words
	remove_words = df['title'][0].split()
	remove_words.append('movie')
	remove_words.append('film')
	remove_words.append('qv')
	remove_words.append('_')
	remove_words

	for word in remove_words:
	    text = text.replace(word,"")

	word_cloud = WordCloud(collocations = False, background_color = 'white').generate(text)


	return word_cloud

"""
plots a wordcloud object
"""
def plot_word_cloud(word_cloud):

	plt.imshow(word_cloud, interpolation='bilinear')
	plt.axis("off")
	plt.show()