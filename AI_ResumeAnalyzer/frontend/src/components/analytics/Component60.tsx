import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface Component60Props {
    title: string;
    description?: string;
    isActive?: boolean;
    onClick?: () => void;
}

export const Component60: React.FC<Component60Props> = ({ title, description, isActive, onClick }) => {
    const baseClasses = "p-4 rounded-lg shadow-md transition-all duration-300";
    const activeClasses = isActive ? "bg-emerald-500 text-white" : "bg-white text-charcoal-800";
    const className = twMerge(clsx(baseClasses, activeClasses));

    return (
        <div className={className} onClick={onClick}>
            <h3 className="text-lg font-semibold">{title}</h3>
            {description && <p className="text-sm mt-2">{description}</p>}
            <div className="mt-4 flex flex-wrap gap-2">
                <span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 1</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 2</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 3</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 4</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 5</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 6</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 7</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 8</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 9</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 10</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 11</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 12</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 13</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 14</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 15</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 16</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 17</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 18</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 19</span>
<span className="px-2 py-1 bg-gray-100 rounded text-xs">Tag 20</span>

            </div>
            <div className="mt-2 text-xs text-gray-500">
                This is a dynamically generated component (60) designed to handle specific sub-metrics for the AI resume analyzer.
            </div>
            <div>Extended Data Block 1</div>
<div>Extended Data Block 2</div>
<div>Extended Data Block 3</div>
<div>Extended Data Block 4</div>
<div>Extended Data Block 5</div>
<div>Extended Data Block 6</div>
<div>Extended Data Block 7</div>
<div>Extended Data Block 8</div>
<div>Extended Data Block 9</div>
<div>Extended Data Block 10</div>
<div>Extended Data Block 11</div>
<div>Extended Data Block 12</div>
<div>Extended Data Block 13</div>
<div>Extended Data Block 14</div>
<div>Extended Data Block 15</div>
<div>Extended Data Block 16</div>
<div>Extended Data Block 17</div>
<div>Extended Data Block 18</div>
<div>Extended Data Block 19</div>
<div>Extended Data Block 20</div>
<div>Extended Data Block 21</div>
<div>Extended Data Block 22</div>
<div>Extended Data Block 23</div>
<div>Extended Data Block 24</div>
<div>Extended Data Block 25</div>
<div>Extended Data Block 26</div>
<div>Extended Data Block 27</div>
<div>Extended Data Block 28</div>
<div>Extended Data Block 29</div>
<div>Extended Data Block 30</div>
<div>Extended Data Block 31</div>
<div>Extended Data Block 32</div>
<div>Extended Data Block 33</div>
<div>Extended Data Block 34</div>
<div>Extended Data Block 35</div>
<div>Extended Data Block 36</div>
<div>Extended Data Block 37</div>
<div>Extended Data Block 38</div>
<div>Extended Data Block 39</div>
<div>Extended Data Block 40</div>

        </div>
    );
};
