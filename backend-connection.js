/**
 * This file handles communication between the frontend and your Python backend
 * You'll need to replace placeholder code with actual implementation based on your setup
 */

class BackendService {
    constructor(backendUrl = 'http://localhost:5000') {
        this.backendUrl = backendUrl;
        this.connected = false;
        this.connectionPromise = this.connect();
    }

    /**
     * Establish connection with the backend
     */
    async connect() {
        try {
            // In a real implementation, you might do a health check
            const response = await fetch(`${this.backendUrl}/health`);
            
            if (response.ok) {
                console.log('Connected to Python backend successfully');
                this.connected = true;
                return true;
            } else {
                throw new Error('Backend service unavailable');
            }
        } catch (error) {
            console.error('Failed to connect to backend:', error);
            this.connected = false;
            return false;
        }
    }

    /**
     * Send a message to the backend and get response
     * @param {string} message - User's message
     * @returns {Promise<string>} - Bot's response
     */
    async sendMessage(message) {
        // Wait for connection first
        if (!this.connected) {
            await this.connectionPromise;
            if (!this.connected) {
                throw new Error('Not connected to backend');
            }
        }

        try {
            const response = await fetch(`${this.backendUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    /**
     * Disconnect from the backend
     */
    disconnect() {
        this.connected = false;
        console.log('Disconnected from backend');
    }
}

// Create a singleton instance
const backendService = new BackendService();
export default backendService;