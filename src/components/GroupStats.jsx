import React from 'react';
import { Users, Eye, TrendingUp } from 'lucide-react';
const GroupStats = ({ groupName, memberCount, games }) => {
    const totalVisits = games.reduce((acc, game) => acc + (game.placeVisits || 0), 0);
    const totalPlaying = games.reduce((acc, game) => acc + (game.playing || 0), 0);
    return (
        <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-white">{groupName}</h2>
                <div className="flex items-center gap-4 text-sm text-gray-400">
                    <div className="flex items-center gap-1.5">
                        <Users size={14} />
                        <span className="font-medium">{memberCount.toLocaleString()}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                        <Eye size={14} />
                        <span className="font-medium">{totalVisits.toLocaleString()}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                        <TrendingUp size={14} />
                        <span className="font-medium">{totalPlaying}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default GroupStats;
