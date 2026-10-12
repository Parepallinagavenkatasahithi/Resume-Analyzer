import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

export default function Layout() {
  return (
    <div className="min-h-screen bg-[#F8F7FC] text-[#18181B] font-sans flex">
      <Sidebar />
      <div className="flex-1 flex flex-col ml-64 min-h-screen">
        <Header />
        <main className="flex-1 p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}