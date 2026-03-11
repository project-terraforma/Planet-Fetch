import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import util from 'util';

const execPromise = util.promisify(exec);

export async function POST(req: Request) {
    try {
        const { release, format = 'default' } = await req.json();

        if (!release) {
            return NextResponse.json({ error: 'Release date is required' }, { status: 400 });
        }

        // Define paths
        const projectRoot = process.cwd();
        
        // Map format to filename
        let filename = 'context.txt';
        if (format === 'v1') filename = 'v1_refined.txt';
        else if (format === 'v2') filename = 'v2_hierarchical.txt';
        else if (format === 'v3') filename = 'v3_tabular.txt';
        else if (format === 'v4') filename = 'v4_compressed.txt';

        const contextFilePath = path.join(projectRoot, 'contexts', release, filename);

        console.log(`Retrieving context for release: ${release}, format: ${format}`);

        // Check if the context file exists
        if (!fs.existsSync(contextFilePath)) {
            return NextResponse.json({ 
                error: `Context file (${format}) not found for release ${release}. Make sure it was pre-generated.` 
            }, { status: 404 });
        }

        // Read the result and return it to the frontend
        const generatedContext = fs.readFileSync(contextFilePath, 'utf-8');

        return NextResponse.json({ success: true, data: generatedContext });

    } catch (error) {
        console.error('Error retrieving context:', error);
        return NextResponse.json({ error: 'Failed to retrieve context' }, { status: 500 });
    }
}
