
const PROXY_URL = 'https://api.codetabs.com/v1/proxy?quest=';

const FALLBACK_DATA = {
    '35507841': [
        {
            id: 8234606308,
            name: "🏖️ หาดสวรรค์ [NEW!]",
            description: "Paradise Beach Hangout...",
            rootPlace: { id: 99002761413888 },
            placeVisits: 374894,
            playing: 120 // Mock
        },
        {
            id: 7657686182,
            name: "🎄 City Banna [🎅Christmas☃️]",
            description: "Welcome to City Banna!...",
            rootPlace: { id: 114116662845070 },
            placeVisits: 3016350,
            playing: 450 // Mock
        },
        {
            id: 7198410061,
            name: "🌆 Banna Town [Beta]",
            description: "Welcome to Banna Town...",
            rootPlace: { id: 77837537595343 },
            placeVisits: 3814406,
            playing: 300 // Mock
        },
        {
            id: 7125555453,
            name: "Thai Donate 💸 [🎃Halloween]",
            description: "Thai PLS Donate...",
            rootPlace: { id: 115842829430610 },
            placeVisits: 4079131,
            playing: 800 // Mock
        }
    ],
    '6443807': [
        {
            id: 8542980908,
            name: "🎄 ตั้งแคมป์",
            description: "Hangout | Voice Chat...",
            rootPlace: { id: 99947655373223 },
            placeVisits: 3243733,
            playing: 250 // Mock
        }
    ]
};

const FALLBACK_GROUP_DETAILS = {
    '35507841': { memberCount: 37669 },
    '6443807': { memberCount: 29220 }
};

const FALLBACK_VOTES = {
    '8234606308': { upVotes: 431, downVotes: 33 },
    '7657686182': { upVotes: 1200, downVotes: 150 },
    '7198410061': { upVotes: 800, downVotes: 50 },
    '7125555453': { upVotes: 2000, downVotes: 300 },
    '8542980908': { upVotes: 1500, downVotes: 100 }
};

export const fetchGroupGames = async (groupId) => {
    try {
        const response = await fetch(`${PROXY_URL}https://games.roblox.com/v2/groups/${groupId}/games?accessFilter=2&sortOrder=Asc&limit=100`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.warn(`Failed to fetch games for group ${groupId}, using fallback data.`, error);
        return FALLBACK_DATA[groupId] || [];
    }
};

export const fetchGameDetails = async (universeIds) => {
    if (!universeIds.length) return [];
    try {
        const ids = universeIds.join(',');
        const response = await fetch(`${PROXY_URL}https://games.roblox.com/v1/games?universeIds=${ids}`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.warn('Failed to fetch game details', error);
        return [];
    }
}

export const getThumbnailUrl = (placeId) => {
    return `https://tr.rbxcdn.com/30DAY-GameIcon-${placeId}-150x150-PNG`;
}

export const fetchThumbnails = async (universeIds) => {
    if (!universeIds.length) return [];
    try {
        const ids = universeIds.join(',');
        const response = await fetch(`${PROXY_URL}https://thumbnails.roblox.com/v1/games/icons?universeIds=${ids}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.warn('Failed to fetch thumbnails', error);
        return [];
    }
}

export const fetchGroupDetails = async (groupId) => {
    try {
        const response = await fetch(`${PROXY_URL}https://groups.roblox.com/v1/groups/${groupId}`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return data;
    } catch (error) {
        console.warn(`Failed to fetch details for group ${groupId}`, error);
        return FALLBACK_GROUP_DETAILS[groupId] || { memberCount: 0 };
    }
};

export const fetchGameVotes = async (universeIds) => {
    if (!universeIds.length) return {};
    try {
        const ids = universeIds.join(',');
        const response = await fetch(`${PROXY_URL}https://games.roblox.com/v1/games/votes?universeIds=${ids}`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        const votesMap = {};
        data.data.forEach(v => {
            votesMap[v.id] = v;
        });
        return votesMap;
    } catch (error) {
        console.warn('Failed to fetch game votes', error);
        return FALLBACK_VOTES;
    }
};
