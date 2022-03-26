import unittest
from unittest.mock import Mock, patch
from spotify import search_artist, get_data
from genius import get_lyrics
from app import saved_artists, getDB, randomArtist

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

class testCaseNoMocking(unittest.TestCase):
    def setUp(self):
        self.testValidArtist = [
            {
                KEY_INPUT: [
                    "BTOB",
                    "YOASOBI",
                    "ヨルシカ",
                ],
                KEY_EXPECTED: [
                    "2hcsKca6hCfFMwwdbFvenJ",
                    "64tJ2EAv1R6UaZqc4iOCyj",
                    "4UK2Lzi6fBfUi9rpDt6cik"
                ],
            },
        ]

        self.testLyricsLink = [
            {
                KEY_INPUT: [
                    "Missing You",
                    "怪物",
                    "ただ君に晴れ"
                ],
                KEY_EXPECTED: [
                    "https://genius.com/Diddy-ill-be-missing-you-lyrics",
                    "https://genius.com/Genius-romanizations-yoasobi-monster-kaibutsu-romanized-lyrics",
                    "https://genius.com/Yorushika-just-a-sunny-day-for-you-lyrics"
                ],
            },
        ]

    def testValidArtist(self):
        for test in self.testValidArtist:
            actual_result0 = search_artist(test[KEY_INPUT][0])
            actual_result1 = search_artist(test[KEY_INPUT][1])
            actual_result2 = search_artist(test[KEY_INPUT][2])
            
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(actual_result0["artistID"], expected_result[0])
            self.assertEqual(actual_result1["artistID"], expected_result[1])
            self.assertEqual(actual_result2["artistID"], expected_result[2])

    def testLyricsLink(self):
        for test in self.testLyricsLink:
            actual_result = get_lyrics(test[KEY_INPUT])
            
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(actual_result["lyrics"], expected_result[0])

class testCaseMocking(unittest.TestCase):
    def setUp(self):
    #     self.initial_db_mock = [
    #         saved_artists(username = "User", artist_ID = ""),
    #         saved_artists(username = "User", artist_ID = ""),
    #         saved_artists(username = "User", artist_ID = "")
    #     ]

        self.testWrongLyrics = [
            {
                KEY_INPUT: [
                    "2hcsKca6hCfFMwwdbFvenJ",
                    "64tJ2EAv1R6UaZqc4iOCyj",
                    "4UK2Lzi6fBfUi9rpDt6cik"
                ],
                KEY_EXPECTED: "2hcsKca6hCfFMwwdbFvenJ"
            },
        ]

    def test_get_artist_url(self):
        def not_random_choice(l):
            return l[0]

        for test in self.testWrongLyrics:
            with patch("app.random.choice", not_random_choice):
                actual_result1 = randomArtist(test[KEY_INPUT][1])
                actual_result2 = randomArtist(test[KEY_INPUT][2])
                expected_result = test[KEY_EXPECTED]
                self.assertEqual(actual_result1, expected_result)
                self.assertEqual(actual_result2, expected_result)

    # def testUser(self):
    #     with patch("app.saved_artists.query") as mock_query:
    #         mock_query.all.return_value = self.initial_db_mock
    #         datas = getDB("All")
    #         self.assertEqual(datas, (["User"], []))

if __name__ == '__main__':
    unittest.main()