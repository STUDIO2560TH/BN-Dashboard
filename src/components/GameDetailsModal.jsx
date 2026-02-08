import React from 'react';
import { X, ThumbsUp, ThumbsDown, Calendar, Clock } from 'lucide-react';
const GameDetailsModal = ({ game, votes, onClose }) => {
    if (!game) return null;
    const upVotes = votes?.upVotes || 0;
    const downVotes = votes?.downVotes || 0;
    const totalVotes = upVotes + downVotes;
    const likeRatio = totalVotes > 0 ? Math.round((upVotes / totalVotes) * 100) : 0;
    return (
        <div
            className={`fixed inset-0 bg-black/80 flex items-center justify-center z-50 transition-opacity p-4 ${game ? 'opacity-100' : 'opacity-0 pointer-events-none'
                }`}
            onClick={onClose}
        >
            <div
                className="bg-zinc-900 rounded-2xl p-4 sm:p-6 md:p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-zinc-800 shadow-2xl"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="flex justify-between items-start mb-4 sm:mb-6">
                    <h2 className="text-xl sm:text-2xl font-bold text-white pr-4">{game?.name}</h2>
                    <button
                        onClick={onClose}
                        className="bg-zinc-800 hover:bg-zinc-700 p-2 rounded-lg transition-colors flex-shrink-0"
                    >
                        <X size={20} />
                    </button>
                </div>
                {game?.description && (
                    <div className="mb-4 sm:mb-6">
                        <h3 className="text-base sm:text-lg font-semibold text-gray-300 mb-2">Description</h3>
                        <p className="text-sm sm:text-base text-gray-400 leading-relaxed">{game.description}</p>
                    </div>
                )}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-4 sm:mb-6">
                    <div className="bg-zinc-800 p-3 sm:p-4 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                            <ThumbsUp className="text-green-500" size={18} />
                            <span className="text-sm sm:text-base text-gray-400">Upvotes</span>
                        </div>
                        <p className="text-lg sm:text-xl font-bold">{upVotes.toLocaleString()}</p>
                    </div>
                    <div className="bg-zinc-800 p-3 sm:p-4 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                            <ThumbsDown className="text-red-500" size={18} />
                            <span className="text-sm sm:text-base text-gray-400">Downvotes</span>
                        </div>
                        <p className="text-lg sm:text-xl font-bold">{downVotes.toLocaleString()}</p>
                    </div>
                    <div className="bg-zinc-800 p-3 sm:p-4 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                            <Calendar className="text-blue-500" size={18} />
                            <span className="text-sm sm:text-base text-gray-400">Created</span>
                        </div>
                        <p className="text-sm sm:text-base font-semibold">{new Date(game?.created).toLocaleDateString()}</p>
                    </div>
                    <div className="bg-zinc-800 p-3 sm:p-4 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                            <Clock className="text-purple-500" size={18} />
                            <span className="text-sm sm:text-base text-gray-400">Updated</span>
                        </div>
                        <p className="text-sm sm:text-base font-semibold">{new Date(game?.updated).toLocaleDateString()}</p>
                    </div>
                </div>
                <div className="flex items-center justify-between pt-4 border-t border-zinc-800">
                    <div className="text-sm sm:text-base">
                        <span className="text-gray-400">Like Ratio: </span>
                        <span className="text-white font-bold">{likeRatio}%</span>
                    </div>
                    <a
                        href={`https://www.roblox.com/games/${game?.rootPlaceId}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg font-bold transition-colors text-sm sm:text-base"
                    >
                        Play Game
                    </a>
                </div>
            </div>
        </div>
    );
};
export default GameDetailsModal;
