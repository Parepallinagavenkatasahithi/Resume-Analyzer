import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Feature Component 21
export interface Feature21Props {
    userId: string;
    isActive: boolean;
}

export const FeatureComponent21: React.FC<Feature21Props> = ({ userId, isActive }) => {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        let mounted = true;
        const fetchData = async () => {
            if (!isActive) return;
            setLoading(true);
            try {
                const result = await axios.get("/api/feature21/" + userId);
                if (mounted) setData(result.data);
            } catch (err: any) {
                if (mounted) setError(err.message || 'Error loading feature data');
            } finally {
                if (mounted) setLoading(false);
            }
        };
        fetchData();
        return () => { mounted = false; };
    }, [userId, isActive]);

    const handleAction = () => {
        console.log("Action triggered on feature 21");
    };

    if (!isActive) return <div className="hidden">Inactive</div>;
    if (loading) return <div className="p-4 flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div></div>;
    if (error) return <div className="text-red-500 p-4 border border-red-200 rounded bg-red-50">{error}</div>;

    return (
        <div className="bg-white rounded-xl shadow-sm p-6 mb-4 border border-gray-100 transition-all hover:shadow-md">
            <h3 className="text-xl font-semibold text-charcoal-800 mb-4">Interactive Feature 21</h3>
            <div className="space-y-4">
                <div className="flex justify-between items-center border-b pb-2">
                    <span className="text-gray-600">Status</span>
                    <span className="px-2 py-1 bg-emerald-100 text-emerald-700 rounded text-sm font-medium">Active</span>
                </div>
                <div className="grid grid-cols-2 gap-4 mt-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-500 mb-1">Metric Alpha</p>
                        <p className="text-lg font-bold text-charcoal-900">{data ? data.alpha : '0.00'}</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-500 mb-1">Metric Beta</p>
                        <p className="text-lg font-bold text-charcoal-900">{data ? data.beta : '0.00'}</p>
                    </div>
                </div>
                <button 
                    onClick={handleAction}
                    className="w-full mt-4 py-2 bg-charcoal-800 hover:bg-charcoal-900 text-white rounded-lg transition-colors font-medium"
                >
                    Refresh Data Pipeline
                </button>
            </div>
        </div>
    );
};
