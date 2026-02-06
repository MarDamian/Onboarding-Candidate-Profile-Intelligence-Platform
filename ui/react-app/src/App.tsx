import { Routes, Route } from 'react-router-dom'
import './App.css'
import { CreatePage } from './pages/Create'
import { EditPage } from './pages/Edit'
import { ShowPage } from './pages/Show'
import { ListPage } from './pages/List'
import { Navbar } from './components/layout/Navbar'
import { Sidebar } from './components/layout/Sidebar'

function App() {
  return (
    <div className='flex min-h-screen bg-slate-50'>
      <div className='shrink-0'>
        <Sidebar />
      </div>
      <div>
        <Navbar />
        <main className='overflow-auto p-4 md:p-6 bg-zinc-100/10 min-w-full'>
          <Routes>
            <Route path="/" element={<ListPage />} />
            <Route path="/create" element={<CreatePage />} />
            <Route path="/edit/:id" element={<EditPage />} />
            <Route path="/:id/insight" element={<ShowPage />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App
