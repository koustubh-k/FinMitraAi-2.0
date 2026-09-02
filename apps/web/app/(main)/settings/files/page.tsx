"use client"

import { useState } from "react"
import { Upload, FileText, X, AlertCircle } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { apiClient } from "@/lib/api-client"
import { toast } from "sonner"

export default function SettingsFilesPage() {
  const [isDragging, setIsDragging] = useState(false)
  const [files, setFiles] = useState<{name: string, progress: number, status: 'uploading' | 'done' | 'error'}[]>([])

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const onDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files))
    }
  }
  
  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(Array.from(e.target.files))
    }
  }

  const handleFiles = (newFiles: File[]) => {
    const newFilesList = newFiles.map(file => ({
      name: file.name,
      progress: 0,
      status: 'uploading' as const
    }))
    
    setFiles(prev => [...prev, ...newFilesList])
    
    // Upload each file
    newFiles.forEach(async (file, idx) => {
      const formData = new FormData();
      formData.append('file', file);
      
      try {
        // Fake progress while waiting for the API
        const interval = setInterval(() => {
          setFiles(prev => {
            const newArr = [...prev];
            const targetIdx = newArr.findIndex(f => f.name === file.name);
            if (targetIdx >= 0 && newArr[targetIdx].progress < 90) {
              newArr[targetIdx].progress += 10;
            }
            return newArr;
          })
        }, 500);

        await apiClient.post("/api/v1/documents/upload", formData);
        
        clearInterval(interval);
        
        setFiles(prev => {
          const newArr = [...prev];
          const targetIdx = newArr.findIndex(f => f.name === file.name);
          if (targetIdx >= 0) {
            newArr[targetIdx].progress = 100;
            newArr[targetIdx].status = 'done';
          }
          return newArr;
        });
        toast.success(`Successfully uploaded ${file.name}`);
        
      } catch (error) {
        setFiles(prev => {
          const newArr = [...prev];
          const targetIdx = newArr.findIndex(f => f.name === file.name);
          if (targetIdx >= 0) {
            newArr[targetIdx].status = 'error';
          }
          return newArr;
        });
        toast.error(`Failed to upload ${file.name}`);
        console.error("Upload error:", error);
      }
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">File Intelligence</h3>
        <p className="text-sm text-muted-foreground">
          Upload documents for FinMitra AI to analyze and reference.
        </p>
      </div>
      <Separator />
      
      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Upload Documents</CardTitle>
            <CardDescription>
              Drag and drop PDF, CSV, or Text files here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div 
              className={`border-2 border-dashed rounded-lg p-12 text-center flex flex-col items-center justify-center transition-colors ${
                isDragging ? 'border-primary bg-primary/5' : 'border-muted-foreground/25'
              }`}
              onDragOver={onDragOver}
              onDragLeave={onDragLeave}
              onDrop={onDrop}
            >
              <Upload className="h-10 w-10 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-1">Click to upload or drag and drop</h3>
              <p className="text-sm text-muted-foreground mb-4">
                PDF, CSV, TXT (max. 10MB)
              </p>
              
              <label htmlFor="file-upload">
                <Button variant="outline" className="cursor-pointer" type="button" onClick={() => document.getElementById('file-upload')?.click()}>
                  Select Files
                </Button>
                <input 
                  id="file-upload" 
                  type="file" 
                  className="hidden" 
                  multiple 
                  accept=".pdf,.csv,.txt"
                  onChange={onFileChange}
                />
              </label>
            </div>
            
            {files.length > 0 && (
              <div className="mt-8 space-y-4">
                <h4 className="text-sm font-medium">Upload Queue</h4>
                {files.map((file, i) => (
                  <div key={i} className="flex items-center gap-4 p-3 rounded-lg border bg-card">
                    <div className="bg-primary/10 p-2 rounded-full">
                      <FileText className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex-1 space-y-1">
                      <div className="flex justify-between items-center text-sm font-medium">
                        <span className="truncate max-w-[200px]">{file.name}</span>
                        {file.status === 'done' ? (
                          <span className="text-success text-xs">Complete</span>
                        ) : file.status === 'error' ? (
                          <span className="text-destructive text-xs">Failed</span>
                        ) : (
                          <span className="text-muted-foreground text-xs">{file.progress}%</span>
                        )}
                      </div>
                      <Progress value={file.progress} className="h-1" />
                    </div>
                    {file.status === 'done' && (
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground">
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
