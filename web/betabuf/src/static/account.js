document.addEventListener('DOMContentLoaded', () => {
    const protoDefinition = `
        syntax = "proto3";
        package game.data;

        message AccountDetails {
            string username = 1;
            string country = 2;
        }
        
        message AccountToken {
            string user_id = 1;
            string username = 2;
            bool is_admin = 3;
            bool is_verified = 4;
        }

        message SecureConnectionDetails {
            bool is_local_ip = 1;
            string id = 2;
        }
    `;

    const root = protobuf.parse(protoDefinition).root;
    const AccountDetails = root.lookupType("game.data.AccountDetails");
    const AccountToken = root.lookupType("game.data.AccountToken");
    
    const output = document.getElementById('output');

    const highScore = parseInt(localStorage.getItem('high_score'), 10) || 0;
    
    function log(message) {
        const content = typeof message === 'object' ? JSON.stringify(message, null, 2) : message;
        output.textContent = content;
        console.log(message);
    }
    
    function createProtobufHex(messageType, payload) {
        const errMsg = messageType.verify(payload);
        if (errMsg) {
            throw Error(`Protobuf verification error: ${errMsg}`);
        }
        const message = messageType.create(payload);
        const buffer = messageType.encode(message).finish();
        return Array.from(buffer).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    function hexToUint8Array(hexString) {
        if (hexString.length % 2 !== 0) {
            throw "Invalid hexString";
        }
        const arrayBuffer = new Uint8Array(hexString.length / 2);
        for (let i = 0; i < hexString.length; i += 2) {
            arrayBuffer[i / 2] = parseInt(hexString.substr(i, 2), 16);
        }
        return arrayBuffer;
    }

    function updateStatusDisplay() {
        const userIdElem = document.getElementById('status-user-id');
        const usernameElem = document.getElementById('status-username');
        const isVerifiedElem = document.getElementById('status-is-verified');
        const highScoreTitleElem = document.getElementById('high-score-title');

        highScoreTitleElem.textContent = `Submit High Score (${highScore} points)`;

        const accountTokenHex = localStorage.getItem('account_token');
        if (accountTokenHex) {
            try {
                const tokenBytes = hexToUint8Array(accountTokenHex);
                const decodedToken = AccountToken.decode(tokenBytes);
                userIdElem.textContent = decodedToken.userId;
                usernameElem.textContent = decodedToken.username;
                isVerifiedElem.textContent = decodedToken.isVerified;
            } catch (e) {
                console.error("Failed to decode account token:", e);
                userIdElem.textContent = 'Error decoding token';
                usernameElem.textContent = 'Error';
                isVerifiedElem.textContent = 'Error';
            }
        } else {
            userIdElem.textContent = 'N/A';
            usernameElem.textContent = 'N/A';
            isVerifiedElem.textContent = 'N/A';
        }
    }

    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('reg-username').value;
        const country = document.getElementById('reg-country').value;
        const fullInvite = document.getElementById('reg-invite-full').value.trim();

        const registration_invite = fullInvite;

        try {
            const accountDetailsHex = createProtobufHex(AccountDetails, { username, country });
            
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    account_details: accountDetailsHex,
                    registration_invite
                })
            });

            const result = await response.json();
            log(result);

            if (response.ok) {
                localStorage.setItem('account_token', result.token);
                localStorage.setItem('account_token_sig', result.signature);
                updateStatusDisplay();
            }
        } catch (error) {
            log(`Error: ${error.message}`);
        }
    });

    document.getElementById('score-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const account_token = localStorage.getItem('account_token');
        const account_token_sig = localStorage.getItem('account_token_sig');

        if (!account_token || !account_token_sig) {
            log('Error: Account token or signature not found. Please register first.');
            return;
        }

        try {
            const response = await fetch('/submit_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    score: highScore,
                    account_token,
                    account_token_sig
                })
            });
            const result = await response.json();
            log(result);
        } catch (error) {
            log(`Error: ${error.message}`);
        }
    });

    document.getElementById('rename-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const new_username = document.getElementById('new-username').value;
        const old_user_token = localStorage.getItem('account_token');
        const old_user_token_sig = localStorage.getItem('account_token_sig');
        
        if (!old_user_token || !old_user_token_sig) {
            log('Error: Account token or signature not found. Please register first.');
            return;
        }

        try {
            const response = await fetch('/rename', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    new_username,
                    old_user_token,
                    old_user_token_sig
                })
            });

            const result = await response.json();
            log(result);

            if (response.ok) {
                log('Username updated. New token and signature stored.');
                localStorage.setItem('account_token', result.token);
                localStorage.setItem('account_token_sig', result.signature);
                updateStatusDisplay();
            }
        } catch (error) {
            log(`Error: ${error.message}`);
        }
    });
    
    document.getElementById('clear-storage').addEventListener('click', () => {
        localStorage.clear();
        log('Local storage cleared.');
        updateStatusDisplay();
    });

    updateStatusDisplay();
});
