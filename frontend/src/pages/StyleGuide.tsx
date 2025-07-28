import React, { useState } from 'react';
import { 
  Button, 
  Input, 
  Textarea, 
  Select, 
  Card, 
  LoadingSpinner 
} from '../components/ui';
import { MessageBubble } from '../components/chat';
import { TransparencyPanel, ProcessingStage } from '../components/transparency';
import { theme } from '../styles/theme';
import type { Message, TransparencyState } from '../types';

const StyleGuide: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [textareaValue, setTextareaValue] = useState('');
  const [selectValue, setSelectValue] = useState('');

  // Demo data for chat components
  const demoUserMessage: Message = {
    id: '1',
    role: 'user',
    content: 'What is the capital of France?',
    timestamp: new Date(),
  };

  const demoAssistantMessage: Message = {
    id: '2',
    role: 'assistant',
    content: 'The capital of France is Paris. It is located in the north-central part of the country and is known for its rich history, culture, and iconic landmarks such as the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral.',
    timestamp: new Date(),
  };

  // Demo data for transparency components
  const demoTransparencyState: TransparencyState = {
    isActive: true,
    progress: 0.6,
    stages: [
      {
        id: '1',
        name: 'Question Processing',
        description: 'Analyzing and understanding your question...',
        status: 'completed',
        icon: '🤔',
        timestamp: new Date(),
      },
      {
        id: '2',
        name: 'Document Retrieval',
        description: 'Searching through knowledge base for relevant information...',
        status: 'completed',
        icon: '🔍',
        timestamp: new Date(),
      },
      {
        id: '3',
        name: 'Context Generation',
        description: 'Organizing retrieved information into context...',
        status: 'in_progress',
        icon: '📝',
        timestamp: new Date(),
      },
      {
        id: '4',
        name: 'Response Generation',
        description: 'Generating comprehensive response based on context...',
        status: 'pending',
        icon: '💭',
      },
    ],
    currentStage: {
      id: '3',
      name: 'Context Generation',
      description: 'Organizing retrieved information into context...',
      status: 'in_progress',
      icon: '📝',
      timestamp: new Date(),
    },
  };

  const selectOptions = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3 (Disabled)', disabled: true },
    { value: 'option4', label: 'Option 4' },
  ];

  const ColorPalette = ({ title, colors }: { title: string; colors: Record<string, string> }) => (
    <div className="mb-8">
      <h3 className="text-lg font-light text-dark-200 mb-4">{title}</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {Object.entries(colors).map(([name, value]) => (
          <div key={name} className="text-center">
            <div 
              className="w-full h-16 rounded-lg border border-dark-600 mb-2"
              style={{ backgroundColor: value }}
            />
            <p className="text-sm font-light text-dark-300">{name}</p>
            <p className="text-xs font-light text-dark-400">{value}</p>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-12">
        <h1 className="text-4xl font-light text-dark-50 mb-4">
          Design System & Style Guide
        </h1>
        <p className="text-lg text-dark-300 font-light">
          A comprehensive guide to the components, colors, and typography used in this application.
        </p>
      </div>

      {/* Color System */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Color System
        </h2>
        
        <ColorPalette 
          title="Primary Colors" 
          colors={theme.colors.primary} 
        />
        
        <ColorPalette 
          title="Dark Theme Colors" 
          colors={theme.colors.dark} 
        />
        
        <ColorPalette 
          title="Button Colors" 
          colors={theme.colors.button} 
        />

        <div className="mb-8">
          <h3 className="text-lg font-light text-dark-200 mb-4">Status Colors</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries({
              success: theme.colors.success,
              warning: theme.colors.warning,
              error: theme.colors.error,
              info: theme.colors.info,
            }).map(([name, value]) => (
              <div key={name} className="text-center">
                <div 
                  className="w-full h-16 rounded-lg border border-dark-600 mb-2"
                  style={{ backgroundColor: value }}
                />
                <p className="text-sm font-light text-dark-300 capitalize">{name}</p>
                <p className="text-xs font-light text-dark-400">{value}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Typography */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Typography
        </h2>
        
        <Card className="mb-6">
          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-thin text-dark-50 mb-2">Heading 1 - Thin</h1>
              <p className="text-sm text-dark-400">4xl, font-thin (100)</p>
            </div>
            <div>
              <h2 className="text-3xl font-extralight text-dark-50 mb-2">Heading 2 - Extra Light</h2>
              <p className="text-sm text-dark-400">3xl, font-extralight (200)</p>
            </div>
            <div>
              <h3 className="text-2xl font-light text-dark-50 mb-2">Heading 3 - Light</h3>
              <p className="text-sm text-dark-400">2xl, font-light (300)</p>
            </div>
            <div>
              <h4 className="text-xl font-normal text-dark-50 mb-2">Heading 4 - Normal</h4>
              <p className="text-sm text-dark-400">xl, font-normal (400)</p>
            </div>
            <div>
              <p className="text-base font-light text-dark-200 mb-2">Body text - Light weight for better readability</p>
              <p className="text-sm text-dark-400">base, font-light (300)</p>
            </div>
            <div>
              <p className="text-sm font-light text-dark-300 mb-2">Small text - Used for captions and secondary information</p>
              <p className="text-sm text-dark-400">sm, font-light (300)</p>
            </div>
          </div>
        </Card>
      </section>

      {/* Buttons */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Buttons
        </h2>
        
        <Card className="mb-6">
          <div className="space-y-8">
            {/* Button Variants */}
            <div>
              <h3 className="text-lg font-light text-dark-200 mb-4">Variants</h3>
              <div className="flex flex-wrap gap-4">
                <Button variant="primary">Primary Button</Button>
                <Button variant="secondary">Secondary Button</Button>
                <Button variant="tertiary">Tertiary Button</Button>
                <Button variant="ghost">Ghost Button</Button>
              </div>
            </div>

            {/* Button Sizes */}
            <div>
              <h3 className="text-lg font-light text-dark-200 mb-4">Sizes</h3>
              <div className="flex flex-wrap items-center gap-4">
                <Button size="sm">Small</Button>
                <Button size="md">Medium</Button>
                <Button size="lg">Large</Button>
              </div>
            </div>

            {/* Button States */}
            <div>
              <h3 className="text-lg font-light text-dark-200 mb-4">States</h3>
              <div className="flex flex-wrap gap-4">
                <Button>Normal</Button>
                <Button loading>Loading</Button>
                <Button disabled>Disabled</Button>
              </div>
            </div>
          </div>
        </Card>
      </section>

      {/* Form Components */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Form Components
        </h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <div className="space-y-6">
              <h3 className="text-lg font-light text-dark-200">Input Fields</h3>
              
              <Input
                label="Text Input"
                placeholder="Enter text here..."
                value={inputValue}
                onChange={setInputValue}
              />
              
              <Input
                label="Input with Error"
                placeholder="This field has an error"
                error="This field is required"
              />
              
              <Input
                label="Disabled Input"
                placeholder="This is disabled"
                disabled
              />
            </div>
          </Card>

          <Card>
            <div className="space-y-6">
              <h3 className="text-lg font-light text-dark-200">Textarea & Select</h3>
              
              <Textarea
                label="Textarea"
                placeholder="Enter longer text here..."
                value={textareaValue}
                onChange={setTextareaValue}
                rows={3}
              />
              
              <Select
                label="Select Dropdown"
                placeholder="Choose an option..."
                value={selectValue}
                onChange={setSelectValue}
                options={selectOptions}
              />
            </div>
          </Card>
        </div>
      </section>

      {/* Cards */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Cards
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card padding="sm" shadow="sm">
            <h3 className="font-light text-dark-100 mb-2">Small Card</h3>
            <p className="text-sm text-dark-300 font-light">
              Small padding and shadow
            </p>
          </Card>
          
          <Card padding="md" shadow="md">
            <h3 className="font-light text-dark-100 mb-2">Medium Card</h3>
            <p className="text-sm text-dark-300 font-light">
              Medium padding and shadow (default)
            </p>
          </Card>
          
          <Card padding="lg" shadow="lg">
            <h3 className="font-light text-dark-100 mb-2">Large Card</h3>
            <p className="text-sm text-dark-300 font-light">
              Large padding and shadow
            </p>
          </Card>
        </div>
      </section>

      {/* Loading States */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Loading States
        </h2>
        
        <Card>
          <div className="space-y-6">
            <h3 className="text-lg font-light text-dark-200">Loading Spinners</h3>
            <div className="flex items-center gap-8">
              <div className="text-center">
                <LoadingSpinner size="sm" className="text-primary-blue mb-2" />
                <p className="text-sm text-dark-400">Small</p>
              </div>
              <div className="text-center">
                <LoadingSpinner size="md" className="text-primary-purple mb-2" />
                <p className="text-sm text-dark-400">Medium</p>
              </div>
              <div className="text-center">
                <LoadingSpinner size="lg" className="text-primary-blue mb-2" />
                <p className="text-sm text-dark-400">Large</p>
              </div>
            </div>
          </div>
        </Card>
      </section>

      {/* Chat Components */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Chat Components
        </h2>
        
        <div className="space-y-8">
          <div>
            <h3 className="text-lg font-light text-dark-200 mb-4">Message Bubbles</h3>
            <Card>
              <div className="space-y-4">
                <MessageBubble message={demoUserMessage} />
                <MessageBubble message={demoAssistantMessage} />
                <MessageBubble 
                  message={{
                    id: 'typing',
                    role: 'assistant',
                    content: '',
                    timestamp: new Date(),
                  }}
                  isTyping={true}
                />
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Transparency Components */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Transparency & Processing
        </h2>
        
        <div className="space-y-8">
          <div>
            <h3 className="text-lg font-light text-dark-200 mb-4">Transparency Panel</h3>
            <TransparencyPanel transparencyState={demoTransparencyState} />
          </div>

          <div>
            <h3 className="text-lg font-light text-dark-200 mb-4">Individual Processing Stages</h3>
            <Card>
              <div className="space-y-4">
                <ProcessingStage 
                  stage={demoTransparencyState.stages[0]} 
                />
                <ProcessingStage 
                  stage={demoTransparencyState.stages[2]} 
                  isActive={true}
                />
                <ProcessingStage 
                  stage={demoTransparencyState.stages[3]} 
                />
                <ProcessingStage 
                  stage={{
                    id: 'error-demo',
                    name: 'Error Example',
                    description: 'This stage encountered an error during processing.',
                    status: 'error',
                    icon: '❌',
                    timestamp: new Date(),
                  }}
                />
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Usage Guidelines */}
      <section className="mb-16">
        <h2 className="text-2xl font-light text-dark-100 mb-8 border-b border-dark-700 pb-2">
          Usage Guidelines
        </h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <h3 className="text-lg font-light text-dark-100 mb-4">✅ Do's</h3>
            <ul className="space-y-2 text-sm text-dark-300 font-light">
              <li>• Use primary buttons for main actions</li>
              <li>• Use secondary buttons for alternative actions</li>
              <li>• Keep font weights light for better readability</li>
              <li>• Use proper spacing between components</li>
              <li>• Maintain consistent border radius</li>
              <li>• Use loading states for async operations</li>
            </ul>
          </Card>
          
          <Card>
            <h3 className="text-lg font-light text-dark-100 mb-4">❌ Don'ts</h3>
            <ul className="space-y-2 text-sm text-dark-300 font-light">
              <li>• Don't use multiple primary buttons in the same section</li>
              <li>• Don't use heavy font weights excessively</li>
              <li>• Don't ignore loading and error states</li>
              <li>• Don't use conflicting color combinations</li>
              <li>• Don't forget to handle disabled states</li>
              <li>• Don't use too many different shadows</li>
            </ul>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default StyleGuide;