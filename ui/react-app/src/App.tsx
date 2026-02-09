import { Routes, Route } from 'react-router-dom'
import './App.css'
import { CreatePage } from './pages/Create'
import { EditPage } from './pages/Edit'
import { ShowPage } from './pages/Show'
import { HeroUIProvider } from "@heroui/react"
import { HomePage } from './pages/Home'
import { AppSidebar } from './components/layout/AppSidebar'
import AppNavbar from './components/layout/AppNavbar'
import { useState } from 'react'

function App() {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <HeroUIProvider>
      <div className='flex min-h-screen'>
        <AppSidebar />
        <div className='flex flex-col w-full'>
          <AppNavbar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
          <main className='overflow-auto p-4 md:p-6 lg:pt-6 pt-16'>
            <Routes>
              <Route path="/" element={<HomePage searchTerm={searchTerm} />} />
              <Route path="/create" element={<CreatePage />} />
              <Route path="/edit/:id" element={<EditPage />} />
              <Route path="/:id/insight" element={<ShowPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </HeroUIProvider>
  )
}

export default App
