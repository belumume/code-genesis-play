
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  Rocket, 
  Brain, 
  Code2, 
  Gamepad2, 
  Sparkles, 
  Terminal, 
  FileText, 
  Zap,
  Play,
  Download,
  Clock,
  CheckCircle
} from "lucide-react";
import { toast } from "sonner";

const Index = () => {
  const [gamePrompt, setGamePrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState("");
  const [generatedGame, setGeneratedGame] = useState(null);

  const handleGenerate = async () => {
    if (!gamePrompt.trim()) {
      toast.error("Please enter a game concept!");
      return;
    }

    setIsGenerating(true);
    setProgress(0);
    setCurrentPhase("Initializing Genesis Engine...");

    // Simulate the AI generation process
    const phases = [
      { name: "Conceptualizing game design...", duration: 2000 },
      { name: "Generating Game Design Document...", duration: 1500 },
      { name: "Creating technical architecture...", duration: 1800 },
      { name: "Planning asset specifications...", duration: 1200 },
      { name: "Writing game code...", duration: 3000 },
      { name: "Optimizing and testing...", duration: 1500 },
      { name: "Finalizing project structure...", duration: 1000 }
    ];

    let totalProgress = 0;
    const progressPerPhase = 100 / phases.length;

    for (const phase of phases) {
      setCurrentPhase(phase.name);
      await new Promise(resolve => setTimeout(resolve, phase.duration));
      totalProgress += progressPerPhase;
      setProgress(Math.min(totalProgress, 100));
    }

    // Simulate completion
    setCurrentPhase("Generation complete!");
    setGeneratedGame({
      name: gamePrompt.split(' ').slice(0, 3).join('_').toLowerCase(),
      files: ['main.py', 'GDD.md', 'TECH_PLAN.md', 'ASSETS.md', 'README.md'],
      size: '2.4 KB',
      playable: true
    });
    setIsGenerating(false);
    toast.success("Game generated successfully!");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900">
      {/* Header */}
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-purple-500/20 rounded-lg">
              <Rocket className="h-8 w-8 text-purple-400" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
              AI Genesis Engine
            </h1>
          </div>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Transform a single sentence into a complete, playable 2D game using advanced AI
          </p>
          <div className="flex items-center justify-center gap-2 mt-4">
            <Badge variant="secondary" className="bg-purple-500/20 text-purple-300">
              <Brain className="h-3 w-3 mr-1" />
              Claude 4 Opus
            </Badge>
            <Badge variant="secondary" className="bg-green-500/20 text-green-300">
              <Zap className="h-3 w-3 mr-1" />
              Autonomous
            </Badge>
            <Badge variant="secondary" className="bg-blue-500/20 text-blue-300">
              <Code2 className="h-3 w-3 mr-1" />
              Python + Pygame
            </Badge>
          </div>
        </div>

        {/* Main Interface */}
        <div className="max-w-4xl mx-auto">
          <Tabs defaultValue="generate" className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger value="generate" className="flex items-center gap-2">
                <Sparkles className="h-4 w-4" />
                Generate
              </TabsTrigger>
              <TabsTrigger value="process" className="flex items-center gap-2">
                <Terminal className="h-4 w-4" />
                Process
              </TabsTrigger>
              <TabsTrigger value="about" className="flex items-center gap-2">
                <FileText className="h-4 w-4" />
                About
              </TabsTrigger>
            </TabsList>

            <TabsContent value="generate" className="space-y-6">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-slate-100 flex items-center gap-2">
                    <Gamepad2 className="h-5 w-5 text-purple-400" />
                    Game Concept Input
                  </CardTitle>
                  <CardDescription>
                    Describe your game idea in a single sentence. The AI will handle everything else.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Input
                      placeholder="e.g., A space shooter where you fight alien invaders"
                      value={gamePrompt}
                      onChange={(e) => setGamePrompt(e.target.value)}
                      className="bg-slate-700 border-slate-600 text-slate-100 text-lg py-6"
                      disabled={isGenerating}
                    />
                    <div className="text-sm text-slate-400">
                      Examples: "A platformer with a jumping character collecting coins" • "A puzzle game with matching colored blocks"
                    </div>
                  </div>

                  <Button 
                    onClick={handleGenerate}
                    disabled={isGenerating || !gamePrompt.trim()}
                    className="w-full bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 text-white py-6 text-lg"
                  >
                    {isGenerating ? (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
                        Generating Game...
                      </div>
                    ) : (
                      <div className="flex items-center gap-2">
                        <Sparkles className="h-5 w-5" />
                        Generate Complete Game
                      </div>
                    )}
                  </Button>
                </CardContent>
              </Card>

              {(isGenerating || generatedGame) && (
                <Card className="bg-slate-800/50 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-slate-100">Generation Progress</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-slate-300">{currentPhase}</span>
                        <span className="text-slate-400">{Math.round(progress)}%</span>
                      </div>
                      <Progress value={progress} className="h-2" />
                    </div>

                    {generatedGame && (
                      <Alert className="bg-green-500/10 border-green-500/20">
                        <CheckCircle className="h-4 w-4 text-green-400" />
                        <AlertDescription className="text-green-300">
                          Game "{generatedGame.name}" generated successfully! 
                          {generatedGame.files.length} files created ({generatedGame.size})
                        </AlertDescription>
                      </Alert>
                    )}

                    {generatedGame && (
                      <div className="grid grid-cols-2 gap-4">
                        <Button className="bg-green-600 hover:bg-green-700">
                          <Play className="h-4 w-4 mr-2" />
                          Play Game
                        </Button>
                        <Button variant="outline" className="border-slate-600">
                          <Download className="h-4 w-4 mr-2" />
                          Download Project
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            <TabsContent value="process" className="space-y-6">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-slate-100">AI Generation Process</CardTitle>
                  <CardDescription>
                    How the Genesis Engine transforms prompts into playable games
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {[
                      {
                        phase: "Conceptualization",
                        icon: Brain,
                        description: "AI analyzes your prompt and creates a comprehensive Game Design Document (GDD)",
                        outputs: ["Game mechanics", "Win/lose conditions", "Control scheme", "Visual style"]
                      },
                      {
                        phase: "Technical Planning", 
                        icon: Code2,
                        description: "Generates technical architecture and asset specifications",
                        outputs: ["File structure", "Class hierarchy", "Asset requirements", "Implementation roadmap"]
                      },
                      {
                        phase: "Code Generation",
                        icon: Terminal,
                        description: "Writes complete Python/Pygame code with proper structure and comments",
                        outputs: ["main.py", "Game classes", "Physics system", "Rendering pipeline"]
                      },
                      {
                        phase: "Quality Assurance",
                        icon: CheckCircle,
                        description: "Verifies game completeness and creates project documentation",
                        outputs: ["README.md", "Installation guide", "How to play", "Technical docs"]
                      }
                    ].map((step, index) => (
                      <div key={index} className="flex gap-4 p-4 rounded-lg bg-slate-700/30 border border-slate-600">
                        <div className="p-2 bg-purple-500/20 rounded-lg">
                          <step.icon className="h-5 w-5 text-purple-400" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-slate-100 mb-1">{step.phase}</h3>
                          <p className="text-slate-300 text-sm mb-3">{step.description}</p>
                          <div className="flex flex-wrap gap-1">
                            {step.outputs.map((output, i) => (
                              <Badge key={i} variant="outline" className="text-xs border-slate-500 text-slate-400">
                                {output}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="about" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-slate-800/50 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-slate-100">Project Vision</CardTitle>
                  </CardHeader>
                  <CardContent className="text-slate-300 space-y-3">
                    <p>
                      The Genesis Engine represents a paradigm shift from AI as a tool to AI as a creative partner, 
                      capable of autonomous game development from concept to completion.
                    </p>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-sm">
                        <Clock className="h-4 w-4 text-purple-400" />
                        <span>Sub-minute generation time</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <Gamepad2 className="h-4 w-4 text-green-400" />
                        <span>Immediately playable games</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <Code2 className="h-4 w-4 text-blue-400" />
                        <span>Clean, documented code</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-slate-800/50 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-slate-100">Technical Stack</CardTitle>
                  </CardHeader>
                  <CardContent className="text-slate-300 space-y-3">
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>AI Model:</span>
                        <Badge className="bg-purple-500/20 text-purple-300">Claude 4 Opus</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Game Engine:</span>
                        <Badge className="bg-green-500/20 text-green-300">Python + Pygame</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Architecture:</span>
                        <Badge className="bg-blue-500/20 text-blue-300">Component-based</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Graphics:</span>
                        <Badge className="bg-orange-500/20 text-orange-300">Geometric primitives</Badge>
                      </div>
                    </div>
                    <Separator className="bg-slate-600" />
                    <p className="text-sm">
                      Built for the Lovable AI Showdown, showcasing autonomous AI capabilities
                      in creative domains.
                    </p>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Index;
