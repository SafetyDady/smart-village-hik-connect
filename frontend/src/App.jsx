import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { CameraIcon, LayoutDashboardIcon, Settings } from 'lucide-react'
// Custom GateIcon
const GateIcon = (props) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M18 2v20M6 2v20M2 6h20M2 18h20" />
  </svg>
)
import './App.css'

// Import components
import CameraMonitor from './components/camera/CameraMonitor'
import GateControl from './components/gate/GateControl'
import Dashboard from './components/dashboard/Dashboard'

function App() {
  return (
    <div className="container mx-auto p-4">
      <header className="mb-6">
        <h1 className="text-3xl font-bold">Smart Village HIK Connect</h1>
        <p className="text-muted-foreground">ระบบจัดการรถเข้าออกหมู่บ้าน</p>
      </header>

      <Tabs defaultValue="cameras" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="cameras" className="flex items-center gap-2">
            <CameraIcon className="h-4 w-4" />
            กล้อง ANPR
          </TabsTrigger>
          <TabsTrigger value="gates" className="flex items-center gap-2">
            <GateIcon className="h-4 w-4" />
            ไม้กั้น
          </TabsTrigger>
          <TabsTrigger value="dashboard" className="flex items-center gap-2">
            <LayoutDashboardIcon className="h-4 w-4" />
            แดชบอร์ด
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="cameras">
          <CameraMonitor />
        </TabsContent>
        
        <TabsContent value="gates">
          <GateControl />
        </TabsContent>
        
        <TabsContent value="dashboard">
          <Dashboard />
        </TabsContent>
      </Tabs>

      <footer className="mt-8 text-center text-sm text-muted-foreground">
        <p>© 2025 Smart Village HIK Connect. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App

