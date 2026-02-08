import React, { useEffect, useState } from 'react';
import { fetchGroupGames, fetchGameDetails, fetchThumbnails, fetchGroupDetails, fetchGameVotes } from './services/roblox.js';
import GameCard from './components/GameCard.jsx';
import GroupStats from './components/GroupStats.jsx';
import GameDetailsModal from './components/GameDetailsModal.jsx';
import OverallStats from './components/OverallStats.jsx';
import { LayoutGrid, RefreshCw } from 'lucide-react';
const GROUPS = [
    { id: '35507841', name: 'Gn Studios ∞' },
    { id: '6443807', name: 'Nearo' }
];
function App() {
    const [games, setGames] = useState({});
    const [thumbnails, setThumbnails] = useState({});
    const [groupDetails, setGroupDetails] = useState({});
    const [votes, setVotes] = useState({});
    const [loading, setLoading] = useState(false);
    const [selectedGame, setSelectedGame] = useState(null);
    const [lastUpdate, setLastUpdate] = useState(new Date());
    useEffect(() => {
        const loadData = async () => {
            // setLoading(true); // disabled for smooth updates
            const gamesData = {};
            const detailsData = {};
            const allUniverseIds = [];
            for (const group of GROUPS) {
                // Fetch Games
                const groupGames = await fetchGroupGames(group.id);
                gamesData[group.id] = groupGames;
                groupGames.forEach(g => allUniverseIds.push(g.id));
                // Fetch Group Details
                const details = await fetchGroupDetails(group.id);
                detailsData[group.id] = details;
            }
            // Fetch thumbnails
            const thumbData = await fetchThumbnails(allUniverseIds);
            const thumbMap = {};
            thumbData.forEach(t => {
                thumbMap[t.targetId] = t.imageUrl;
            });
            setThumbnails(thumbMap);
            // Fetch game details (playing counts)
            const details = await fetchGameDetails(allUniverseIds);
            if (details.length) {
                details.forEach(d => {
                    for (const gid in gamesData) {
                        const gameIndex = gamesData[gid].findIndex(g => g.id === d.id);
                        if (gameIndex !== -1) {
                            gamesData[gid][gameIndex] = { ...gamesData[gid][gameIndex], playing: d.playing, created: d.created, updated: d.updated };
                        }
                    }
                });
            }
            // Fetch Votes
            const votesData = await fetchGameVotes(allUniverseIds);
            setVotes(votesData);
            setGames(gamesData);
            setGroupDetails(detailsData);
            // setLoading(false); // disabled
            setLastUpdate(new Date());
        };
        loadData();
        // Auto-refresh every 30 seconds – only update player counts and votes
        const interval = setInterval(async () => {
            // Gather all game IDs currently loaded
            const allIds = Object.values(games).flat().map(g => g.id);
            if (allIds.length === 0) return;
            // Fetch updated playing counts
            const updatedDetails = await fetchGameDetails(allIds);
            if (updatedDetails.length) {
                setGames(prevGames => {
                    const newGames = { ...prevGames };
                    for (const gid in newGames) {
                        newGames[gid] = newGames[gid].map(g => {
                            const detail = updatedDetails.find(d => d.id === g.id);
                            return detail ? { ...g, playing: detail.playing, created: detail.created, updated: detail.updated } : g;
                        });
                    }
                    return newGames;
                });
            }
            // Fetch updated votes
            const updatedVotes = await fetchGameVotes(allIds);
            setVotes(updatedVotes);
        }, 30000);
        // Cleanup interval on unmount
        return () => clearInterval(interval);
    }, []);
    return (
        <div className="min-h-screen bg-[#0f0f0f] text-white p-3 sm:p-6 md:p-8 font-sans">
            <header className="mb-6 sm:mb-10 flex items-center justify-between border-b border-zinc-800 pb-4">
                <div className="flex items-center gap-3">
                    <div className="bg-blue-600 p-2.5 rounded-xl shadow-lg shadow-blue-900/20">
                        <LayoutGrid className="w-6 h-6" />
                    </div>
                    <div>
                        <h1 className="text-xl sm:text-2xl md:text-3xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Roblox Dashboard</h1>
                        <p className="text-xs sm:text-sm text-gray-400">Tracking games for Gn Studios & Nearo</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 text-xs text-gray-500">
                    <RefreshCw className="w-3 h-3 animate-spin" style={{ animationDuration: '3s' }} />
                    <span className="hidden sm:inline">Updates every 30s</span>
                </div>
            </header>
            {loading ? (
                <div className="flex items-center justify-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                </div>
            ) : (
                <div className="space-y-8 sm:space-y-12">
                    <OverallStats groupsData={games} groupDetails={groupDetails} />
                    {GROUPS.map(group => (
                        <section key={group.id}>
                            <GroupStats
                                groupName={group.name}
                                memberCount={groupDetails[group.id]?.memberCount || 0}
                                games={games[group.id] || []}
                            />
                            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-4">
                                {games[group.id]?.map(game => (
                                    <GameCard
                                        key={game.id}
                                        game={game}
                                        thumbnail={thumbnails[game.id]}
                                        onClick={setSelectedGame}
                                    />
                                ))}
                                {(!games[group.id] || games[group.id].length === 0) && (
                                    <p className="text-gray-500 italic col-span-2">No games found.</p>
                                )}
                            </div>
                        </section>
                    ))}
                </div>
            )}
            <GameDetailsModal
                game={selectedGame}
                votes={selectedGame ? votes[selectedGame.id] : null}
                onClose={() => setSelectedGame(null)}
            />
        </div>
    );
}
export default App;
