"""
Data Manager for Minigames Central
Handles persistent storage of high scores, achievements, and player data
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class DataManager:
    def __init__(self, data_file="minigames_data.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        """Load game data from file or create default structure"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self.create_default_data()
        else:
            return self.create_default_data()

    def create_default_data(self) -> Dict[str, Any]:
        """Create default data structure"""
        return {
            "version": "1.0",
            "high_scores": {
                "flappy_bird": [],
                "snake": [],
                "pong": [],
                "monster_run": [],
                "space_invaders": [],
                "tetris": [],
                "2048": [],
                "breakout": []
            },
            "achievements": {
                "first_victory": False,
                "speed_runner": False,
                "survivor": False,
                "explorer": False,
                "adventurer": False,
                "leaderboard_hero": False,
                "legendary": False,
                "week_warrior": False
            },
            "player_stats": {
                "total_games_played": 0,
                "total_playtime": 0,
                "total_score": 0,
                "games_won": 0,
                "favorite_game": None,
                "current_streak": 0,
                "longest_streak": 0
            },
            "game_sessions": []
        }

    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_high_score(self, game_name: str, player_name: str, score: int) -> bool:
        """
        Add a high score for a game
        Returns True if score made top 10
        """
        if game_name not in self.data["high_scores"]:
            return False

        score_entry = {
            "player": player_name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Add score
        self.data["high_scores"][game_name].append(score_entry)

        # Sort by score (descending)
        self.data["high_scores"][game_name].sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # Keep only top 100
        self.data["high_scores"][game_name] = self.data["high_scores"][game_name][:100]

        self.save_data()

        # Check if in top 10
        return len(self.data["high_scores"][game_name]) <= 10

    def get_high_scores(self, game_name: str, limit: int = 10) -> List[Dict]:
        """Get top N high scores for a game"""
        if game_name not in self.data["high_scores"]:
            return []
        return self.data["high_scores"][game_name][:limit]

    def get_personal_best(self, game_name: str) -> int:
        """Get personal best score for a game"""
        if game_name not in self.data["high_scores"]:
            return 0

        scores = self.data["high_scores"][game_name]
        if scores:
            return scores[0]["score"]
        return 0

    def add_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement"""
        if achievement_id not in self.data["achievements"]:
            return False

        if not self.data["achievements"][achievement_id]:
            self.data["achievements"][achievement_id] = True
            self.save_data()
            return True
        return False

    def has_achievement(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked"""
        return self.data["achievements"].get(achievement_id, False)

    def get_achievements(self) -> Dict[str, bool]:
        """Get all achievements"""
        return self.data["achievements"]

    def get_unlocked_count(self) -> int:
        """Get total unlocked achievements"""
        return sum(1 for v in self.data["achievements"].values() if v)

    def update_player_stats(self, game_name: str, score: int, won: bool, playtime: int):
        """Update overall player statistics"""
        stats = self.data["player_stats"]
        stats["total_games_played"] += 1
        stats["total_playtime"] += playtime
        stats["total_score"] += score

        if won:
            stats["games_won"] += 1

        if stats["favorite_game"] is None:
            stats["favorite_game"] = game_name

        self.save_data()

    def add_game_session(self, game_name: str, score: int, duration: int, won: bool):
        """Record a game session"""
        session = {
            "game": game_name,
            "score": score,
            "duration": duration,
            "won": won,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.data["game_sessions"].append(session)

        # Keep only last 100 sessions
        self.data["game_sessions"] = self.data["game_sessions"][-100:]

        self.save_data()

    def get_player_stats(self) -> Dict[str, Any]:
        """Get player statistics"""
        return self.data["player_stats"]

    def export_stats(self) -> Dict[str, Any]:
        """Export all data for analytics"""
        return {
            "high_scores": self.data["high_scores"],
            "achievements": self.data["achievements"],
            "player_stats": self.data["player_stats"],
            "sessions": len(self.data["game_sessions"]),
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def clear_data(self):
        """Clear all data (reset to default)"""
        self.data = self.create_default_data()
        self.save_data()


# Global instance
data_manager = None

def get_data_manager() -> DataManager:
    """Get or create global data manager instance"""
    global data_manager
    if data_manager is None:
        data_manager = DataManager()
    return data_manager
