
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { 
  Gamepad2, 
  Cpu, 
  FileText, 
  Code, 
  Zap, 
  Play,
  Terminal,
  Sparkles,
  CheckCircle,
  Clock
} from "lucide-react";

const Index = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentPhase, setCurrentPhase] = useState<string | null>(null);

  const handleGenerateGame = () => {
    setIsGenerating(true);
    setCurrentPhase("Conceptualizing...");
    
    // Simulate the generation process phases
    setTimeout(() => setCurrentPhase("Planning architecture..."), 2000);
    setTimeout(() => setCurrentPhase("Generating code..."), 4000);
    setTimeout(() => setCurrentPhase("Finalizing game..."), 6000);
    setTimeout(() => {
      setCurrentPhase("Complete!");
      setIsGenerating(false);
    }, 8000);
  };

  const progressValue = currentPhase ? 
    (currentPhase.includes("Conceptualizing") ? 25 :
     currentPhase.includes("Planning") ? 50 :
     currentPhase.includes("Generating") ? 75 :
     currentPhase.includes("Finalizing") ? 90 : 100) : 0;

  const projectStatus = [
    { phase: "Foundation", status: "complete", description: "Core architecture & CLI" },
    { phase: "AI Integration", status: "complete", description: "Claude 4 Opus agent ready" },
    { phase: "Game Generation", status: "ready", description: "End-to-end pipeline" },
    { phase: "Demo & Polish", status: "pending", description: "Video creation & submission" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="h-8 w-8 text-purple-400" />
            <h1 className="text-4xl font-bold text-white">AI Genesis Engine</h1>
            <Sparkles className="h-8 w-8 text-purple-400" />
          </div>
          <p className="text-xl text-gray-300 mb-6">
            Transform single-sentence prompts into complete, playable 2D games
          </p>
          <Badge variant="outline" className="text-purple-300 border-purple-300">
            Phase 2: Core Implementation Ready
          </Badge>
        </div>

        {/* Current Status */}
        <Card className="mb-8 bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Clock className="h-5 w-5 text-green-400" />
              Project Status - Phase 2 Active
            </CardTitle>
            <CardDescription className="text-gray-300">
              Ready for game generation testing and Phase 2 milestones
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {projectStatus.map((item, index) => (
                <div key={index} className="flex items-center gap-3 p-3 rounded-lg bg-slate-700/30">
                  {item.status === "complete" ? (
                    <CheckCircle className="h-5 w-5 text-green-400" />
                  ) : item.status === "ready" ? (
                    <Zap className="h-5 w-5 text-yellow-400" />
                  ) : (
                    <Clock className="h-5 w-5 text-gray-400" />
                  )}
                  <div>
                    <div className="font-medium text-white text-sm">{item.phase}</div>
                    <div className="text-xs text-gray-400">{item.description}</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Demo Interface */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Input Section */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Terminal className="h-5 w-5 text-blue-400" />
                Genesis Engine Demo
              </CardTitle>
              <CardDescription className="text-gray-300">
                Enter a game concept to generate a complete 2D game
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-600">
                <code className="text-green-400 text-sm">
                  python run.py "A space platformer where you collect crystals while avoiding alien enemies"
                </code>
              </div>
              
              {isGenerating && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-white">
                    <Cpu className="h-4 w-4 animate-spin text-purple-400" />
                    <span className="text-sm">{currentPhase}</span>
                  </div>
                  <Progress value={progressValue} className="h-2" />
                </div>
              )}

              <Button 
                onClick={handleGenerateGame}
                disabled={isGenerating}
                className="w-full bg-purple-600 hover:bg-purple-700"
              >
                {isGenerating ? (
                  <>
                    <Cpu className="mr-2 h-4 w-4 animate-spin" />
                    Generating Game...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Generate Game
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Output Preview */}
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Gamepad2 className="h-5 w-5 text-green-400" />
                Generated Output
              </CardTitle>
              <CardDescription className="text-gray-300">
                Complete game project with documentation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-gray-300">
                  <FileText className="h-4 w-4 text-blue-400" />
                  <span className="text-sm">GDD.md - Game Design Document</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <FileText className="h-4 w-4 text-green-400" />
                  <span className="text-sm">TECH_PLAN.md - Technical Architecture</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <FileText className="h-4 w-4 text-yellow-400" />
                  <span className="text-sm">ASSETS.md - Asset Specifications</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <Code className="h-4 w-4 text-purple-400" />
                  <span className="text-sm">main.py - Complete Game Code</span>
                </div>
                
                <Separator className="bg-slate-600" />
                
                <div className="p-3 bg-slate-900/50 rounded border border-slate-600">
                  <div className="text-xs text-gray-400 mb-1">Generated Game Features:</div>
                  <ul className="text-xs text-gray-300 space-y-1">
                    <li>• Complete Pygame implementation</li>
                    <li>• Player movement & physics</li>
                    <li>• Collision detection</li>
                    <li>• Win/lose conditions</li>
                    <li>• Placeholder graphics ready</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Technical Features */}
        <div className="grid md:grid-cols-3 gap-6">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white text-lg flex items-center gap-2">
                <Cpu className="h-5 w-5 text-purple-400" />
                AI Agent Core
              </CardTitle>
            </CardHeader>
            <CardContent className="text-gray-300 text-sm space-y-2">
              <p>• Claude 4 Opus integration</p>
              <p>• Autonomous design & planning</p>
              <p>• Code generation pipeline</p>
              <p>• Memory persistence system</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white text-lg flex items-center gap-2">
                <Code className="h-5 w-5 text-green-400" />
                Game Generation
              </CardTitle>
            </CardHeader>
            <CardContent className="text-gray-300 text-sm space-y-2">
              <p>• Python + Pygame output</p>
              <p>• Complete documentation</p>
              <p>• Placeholder graphics system</p>
              <p>• Playable from generation</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white text-lg flex items-center gap-2">
                <Zap className="h-5 w-5 text-yellow-400" />
                Competition Ready
              </CardTitle>
            </CardHeader>
            <CardContent className="text-gray-300 text-sm space-y-2">
              <p>• CLI & web interface</p>
              <p>• End-to-end pipeline</p>
              <p>• Demo video preparation</p>
              <p>• Hackathon velocity focus</p>
            </CardContent>
          </Card>
        </div>

        {/* Next Steps */}
        <Card className="mt-8 bg-gradient-to-r from-purple-900/20 to-blue-900/20 border-purple-500/30">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-purple-400" />
              Ready for Phase 2 Testing
            </CardTitle>
            <CardDescription className="text-gray-300">
              Core AI agent implemented - ready to generate first game and verify end-to-end pipeline
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <h4 className="font-medium text-white">Immediate Actions:</h4>
                <ul className="text-gray-300 space-y-1">
                  <li>• Test game generation pipeline</li>
                  <li>• Verify generated game quality</li>
                  <li>• Debug any generation issues</li>
                  <li>• Optimize AI prompts for better output</li>
                </ul>
              </div>
              <div className="space-y-2">
                <h4 className="font-medium text-white">Phase 2 Goals:</h4>
                <ul className="text-gray-300 space-y-1">
                  <li>• Complete playable game (Hour 24)</li>
                  <li>• Multiple genre support</li>
                  <li>• Robust error handling</li>
                  <li>• Demo video preparation</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Index;

