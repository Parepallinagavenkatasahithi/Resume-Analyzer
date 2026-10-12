import axios from 'axios';

export const Service91 = {
    getData: async () => {
        const response = await axios.get('/api/service91/data');
        return response.data;
    },
    postData: async (data: any) => {
        const response = await axios.post('/api/service91/data', data);
        return response.data;
    },

    processSubData1: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag1: item.val > 10
        }));
    },

    processSubData2: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag2: item.val > 20
        }));
    },

    processSubData3: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag3: item.val > 30
        }));
    },

    processSubData4: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag4: item.val > 40
        }));
    },

    processSubData5: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag5: item.val > 50
        }));
    },

    processSubData6: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag6: item.val > 60
        }));
    },

    processSubData7: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag7: item.val > 70
        }));
    },

    processSubData8: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag8: item.val > 80
        }));
    },

    processSubData9: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag9: item.val > 90
        }));
    },

    processSubData10: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag10: item.val > 100
        }));
    },

    processSubData11: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag11: item.val > 110
        }));
    },

    processSubData12: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag12: item.val > 120
        }));
    },

    processSubData13: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag13: item.val > 130
        }));
    },

    processSubData14: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag14: item.val > 140
        }));
    },

    processSubData15: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag15: item.val > 150
        }));
    },

    processSubData16: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag16: item.val > 160
        }));
    },

    processSubData17: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag17: item.val > 170
        }));
    },

    processSubData18: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag18: item.val > 180
        }));
    },

    processSubData19: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag19: item.val > 190
        }));
    },

    processSubData20: (input: any) => {
        return input.map((item: any) => ({
            ...item,
            processed: true,
            flag20: item.val > 200
        }));
    },
};
