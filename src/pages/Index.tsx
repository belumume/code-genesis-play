
import { GameGenerator } from "@/components/GameGenerator";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="mb-6">
            <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-purple-400 via-pink-500 to-purple-600 bg-clip-text text-transparent mb-4">
              AI Genesis Engine
            </h1>
            <p className="text-xl md:text-2xl text-slate-300 max-w-3xl mx-auto">
              Transform single-sentence prompts into complete, playable 2D games using the power of Claude AI
            </p>
          </div>
          
          <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-400">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span>Autonomous Game Design</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
              <span>Complete Code Generation</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>Instant Playability</span>
            </div>
          </div>
        </div>

        {/* Game Generator */}
        <GameGenerator />

        {/* Footer */}
        <div className="text-center mt-16 pt-8 border-t border-slate-800">
          <p className="text-slate-500 text-sm">
            Built for the $40,000 AI Showdown • Powered by Claude 4 Opus • 
            <span className="text-purple-400 ml-1">Human-AI Creative Collaboration</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Index;
