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
    const AccountToken = root.lookupType("game.data.AccountToken");
    const SecureConnectionDetails = root.lookupType("game.data.SecureConnectionDetails");

    const output = document.getElementById('output');
    
    function log(message) {
        const content = typeof message === 'object' ? JSON.stringify(message, null, 2) : message;
        output.textContent = content;
        console.log(message);
    }

    /**
     * Converts a hex string to a Uint8Array.
     * @param {string} hexString The hex string to convert.
     * @returns {Uint8Array} The resulting byte array.
     */
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

    /**
     * Updates the status display by decoding tokens from local storage.
     */
    function updateStatusDisplay() {
        const userIdElem = document.getElementById('status-user-id');
        const usernameElem = document.getElementById('status-username');
        const isAdminElem = document.getElementById('status-is-admin');
        const isVerifiedElem = document.getElementById('status-is-verified');
        const secureConnElem = document.getElementById('status-secure-connection');

        const accountTokenHex = localStorage.getItem('account_token');
        if (accountTokenHex) {
            try {
                const tokenBytes = hexToUint8Array(accountTokenHex);
                const decodedToken = AccountToken.decode(tokenBytes);
                userIdElem.textContent = decodedToken.userId;
                usernameElem.textContent = decodedToken.username;
                isAdminElem.textContent = decodedToken.isAdmin;
                isVerifiedElem.textContent = decodedToken.isVerified;
            } catch (e) {
                console.error("Failed to decode account token:", e);
                userIdElem.textContent = 'Error decoding token';
                usernameElem.textContent = 'Error';
                isAdminElem.textContent = 'Error';
                isVerifiedElem.textContent = 'Error';
            }
        } else {
            userIdElem.textContent = 'N/A';
            usernameElem.textContent = 'N/A';
            isAdminElem.textContent = 'N/A';
            isVerifiedElem.textContent = 'N/A';
        }

        const secureConnectionHex = localStorage.getItem('secure_connection_details');
        if (secureConnectionHex) {
            try {
                const connBytes = hexToUint8Array(secureConnectionHex);
                const decodedConn = SecureConnectionDetails.decode(connBytes);
                secureConnElem.textContent = decodedConn.isLocalIp ? 'Established (Local IP)' : 'Failed (Non-Local IP)';
            } catch (e) {
                console.error("Failed to decode secure connection details:", e);
                secureConnElem.textContent = 'Error decoding details';
            }
        } else {
            secureConnElem.textContent = 'Not established';
        }
    }

    document.getElementById('verify-conn-btn').addEventListener('click', async () => {
        try {
            const response = await fetch('/admin/verify-connection');
            const result = await response.json();
            log(result);

            if (response.ok) {
                localStorage.setItem('secure_connection_details', result.secure_connection_details);
                localStorage.setItem('secure_connection_details_sig', result.signature);
                updateStatusDisplay();
            }
        } catch (error) {
            log(`Error: ${error.message}`);
        }
    });

    document.getElementById('get-flag-btn').addEventListener('click', async () => {
        const account_token = localStorage.getItem('account_token');
        const account_token_sig = localStorage.getItem('account_token_sig');
        const secure_connection_details = localStorage.getItem('secure_connection_details');
        const secure_connection_details_sig = localStorage.getItem('secure_connection_details_sig');

        if (!account_token || !secure_connection_details) {
            log('Error: Missing account token or secure connection details.');
            return;
        }
        
        try {
            const response = await fetch('/admin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    account_token,
                    account_token_sig,
                    secure_connection_details,
                    secure_connection_details_sig
                })
            });
            const result = await response.json();
            log(result);
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
