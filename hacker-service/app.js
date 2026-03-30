const axios = require('axios');

const logs = [
    "ERROR: Unauthorized login attempt on /admin/config",
    "CRITICAL: SQL Injection pattern detected in query string",
    "WARNING: Multiple failed SSH attempts from IP 10.0.0.5",
    "INFO: System health check - CPU usage at 85%",
    "ALERT: Suspicious file upload detected in /tmp directory"
];

// In the workshop, this URL will change to your Kubernetes Service Name
const SRE_URL = "http://localhost:5000/log";

console.log(`\n--------------------------------------`);
console.log(`🥷  HACKER SERVICE STARTED`);
console.log(`📡 TARGET: ${SRE_URL}`);
console.log(`--------------------------------------\n`);

setInterval(async () => {
    const randomLog = logs[Math.floor(Math.random() * logs.length)];

    try {
        const response = await axios.post(SRE_URL, { log: randomLog });
        console.log(`[✅ Sent Success]: ${randomLog}`);
        console.log(`[🤖 SRE Response]: ${response.data.advice}\n`);
    } catch (err) {
        // More descriptive error logging
        const status = err.response ? err.response.status : "OFFLINE";
        console.error(`[❌ Connection Error]: SRE Assistant is ${status}`);
    }
}, 15000); // 15 seconds keeps us under the Gemini Free Tier limit