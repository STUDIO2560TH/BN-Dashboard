import React, { useEffect, useState } from 'react';
import { Users, Eye } from 'lucide-react';
const GameCard = ({ game, thumbnail, onClick }) => {
    const [prevPlaying, setPrevPlaying] = useState(game.playing || 0);
    const [animate, setAnimate] = useState(false);
    useEffect(() => {
        if (game.playing !== prevPlaying) {
            setAnimate(true);
            const timer = setTimeout(() => setAnimate(false), 600);
            setPrevPlaying(game.playing);
            return () => clearTimeout(timer);
        }
    }, [game.playing, prevPlaying]);
    return (
        <div
            onClick={() => onClick(game)}
            className="bg-zinc-900 rounded-xl overflow-hidden border border-zinc-800 hover:border-blue-500 transition-all cursor-pointer active:scale-95 sm:hover:scale-105 shadow-lg"
        >
            <div className="relative h-36 sm:h-44 bg-zinc-800">
                <img
                    src={thumbnail || `https://via.placeholder.com/300x200?text=${encodeURIComponent(game.name)}`}
                    alt={game.name}
                    className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
            </div>
            <div className="p-3">
                <h3 className="text-sm font-bold text-white mb-2 line-clamp-2 leading-tight">{game.name}</h3>
                <div className="flex items-center justify-between text-xs text-gray-400">
                    <div className="flex items-center gap-1.5">
                        <Users size={13} className="flex-shrink-0" />
                        <span className={animate ? 'count-change' : ''}>{game.playing || 0}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                        <Eye size={13} className="flex-shrink-0" />
                        <span>{(game.placeVisits || 0).toLocaleString()}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default GameCard;
