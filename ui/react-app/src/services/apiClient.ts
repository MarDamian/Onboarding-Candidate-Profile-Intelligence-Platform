import axios from "axios";

const apiClient = axios.create({
    timeout: 10000,
});

apiClient.interceptors.response.use(undefined, async (err: any) => {
    const { config } = err;

    if (!config || !config.retry) return Promise.reject(err);

    config.__retryCount = config.__retryCount || 0;

    if (config.__retryCount >= config.retry) {
        return Promise.reject(err);
    }

    config.__retryCount += 1;

    const backoff = new Promise((resolve) => {
        setTimeout(() => {
            resolve(null);
        }, config.retryDelay || 1000);
    });

    await backoff;
    console.warn(`Retrying request ${config.url} (Attempt ${config.__retryCount})`);
    return apiClient(config);
});

export default apiClient;
