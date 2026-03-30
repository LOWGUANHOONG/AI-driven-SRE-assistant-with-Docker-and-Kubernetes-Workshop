const axios = require('axios');

const logs = [
    "ERROR: Unauthorized login attempt on /admin/config",
    "CRITICAL: SQL Injection pattern detected in query string",
    "WARNING: Multiple failed SSH attempts from IP 10.0.0.5",
    "INFO: System health check - CPU usage at 85%",
    "ALERT: Suspicious file upload detected in /tmp directory"
];

console.log("Hacker Service Started. Sending logs to http://sre-assistant/log...");

setInterval(async () => {
    const randomLog = logs[Math.floor(Math.random() * logs.length)];

    try {
        // 'sre-assistant' is the K8s Service name we will define in our YAML
        await axios.post('http://sre-assistant/log', { log: randomLog });
        console.log(`[Sent Success]: ${randomLog}`);
    } catch (err) {
        console.error("[Connection Error]: SRE Assistant is offline or K8s Service not ready.");
    }
}, 5000);