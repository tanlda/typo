'use client'

import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import markdown from './markdown'

export default function Home() {
  return (
    <div className="flex h-screen w-full flex-col items-center overflow-y-scroll px-12 py-12">
      <div className="w-full max-w-screen-xl">
        <Markdown remarkPlugins={[remarkGfm]} className="prose min-w-[960px]">
          {markdown}
        </Markdown>
      </div>
    </div>
  )
}
