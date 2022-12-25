import streamlit as st
import pandas as pd
import numpy as np
import tekore
import spotipy
from numpy.linalg import norm
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import os

os.environ['SPOTIPY_CLIENT_ID'] = '5d154fbed7634659a1d6a3ec086a45e2'
os.environ['SPOTIPY_CLIENT_SECRET']='dcec287c49db42bca8679789d5bf587b'




def main():
    SPOTIPY_CLIENT_ID='5d154fbed7634659a1d6a3ec086a45e2'
    SPOTIPY_CLIENT_SECRET='dcec287c49db42bca8679789d5bf587b'
    
    st.title("Let's find a similar song!")
    SONG_NAME = st.text_input("Enter a song")
    
    

    def authorize():
        CLIENT_ID = "5d154fbed7634659a1d6a3ec086a45e2"
        CLIENT_SECRET = "dcec287c49db42bca8679789d5bf587b"
        app_token = tekore.request_client_token(CLIENT_ID, CLIENT_SECRET)
        return tekore.Spotify(app_token)

#    spotifyApi = authorization.authorize()

#    sp1 = spotipy.authorize()
#
#    # Replace YOUR_ACCESS_TOKEN with your access token
#    sp1.token = '5d154fbed7634659a1d6a3ec086a45e2'

    auth_manager = SpotifyClientCredentials()
    sp1 = spotipy.Spotify(auth_manager=auth_manager)

    # Replace SONG_NAME with the name of the song you want to search for
#    scope = "user-library-read"
#    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp1.search(q=f'track:{SONG_NAME}', type='track', )
    # Get the first track from the search results
    track = results['tracks']['items'][0]
    req_uri = track['id']

    df = pd.read_csv("valenceArousalDataset.csv")
    df["mood_vec"] = df[["valence", "energy"]].values.tolist()
    sp = authorize()
    def recommend(track_id, ref_df, sp, n_recs = 5):
    
        track_features = sp.track_audio_features(track_id)
        track_mood_vector = np.array([track_features.valence, track_features.energy])
        
        ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_mood_vector-np.array(x)))
        ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
        ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
        return ref_df_sorted.iloc[:n_recs]
    
    if (SONG_NAME == ""):
        st.write("Please enter a song to find a match")
    else:
        st.write(recommend(req_uri, ref_df=df, sp=sp, n_recs=10)[['trackName','artistName']])

if __name__ == '__main__':
    main()
