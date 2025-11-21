from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

def generate_chat_pdf(chat: list[dict]):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center aligned
        textColor=colors.darkblue
    )
    
    user_style = ParagraphStyle(
        'UserStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.darkblue,
        backColor=colors.lightblue,
        borderPadding=10,
        leftIndent=0,
        rightIndent=100
    )
    
    assistant_style = ParagraphStyle(
        'AssistantStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.darkgreen,
        backColor=colors.lightgrey,
        borderPadding=10,
        leftIndent=100,
        rightIndent=0
    )
    
    timestamp_style = ParagraphStyle(
        'TimestampStyle',
        parent=styles['Italic'],
        fontSize=8,
        textColor=colors.gray
    )
    
    # Title
    title = Paragraph("Chat Export - YouTube Video Assistant", title_style)
    story.append(title)
    
    # Export info
    export_time = Paragraph(f"<i>Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>", styles['Italic'])
    story.append(export_time)
    story.append(Spacer(1, 0.3*inch))
    
    # Chat content
    if not chat:
        story.append(Paragraph("No chat messages to export.", styles['Normal']))
    else:
        for i, message in enumerate(chat):
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            timestamp = message.get('timestamp', '')
            
            # Format timestamp
            try:
                if timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    formatted_time = "Unknown time"
            except:
                formatted_time = "Invalid time"
            
            # Determine speaker label and style
            if role == 'user':
                speaker_label = "👤 You"
                style = user_style
                alignment = "right"
            elif role == 'assistant':
                speaker_label = "🤖 Assistant"
                style = assistant_style
                alignment = "left"
            else:
                speaker_label = "❓ Unknown"
                style = styles['Normal']
                alignment = "left"
            
            # Create message header with speaker and time
            header_text = f"<b>{speaker_label}</b> - {formatted_time}"
            header = Paragraph(header_text, timestamp_style)
            story.append(header)
            
            # Create message content
            if content:
                message_para = Paragraph(content, style)
                story.append(message_para)
            
            # Add spacing between messages
            story.append(Spacer(1, 0.2*inch))
            
            # Add page break every 15 messages to avoid overflow
            if (i + 1) % 15 == 0:
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph("- - - Continued on next page - - -", styles['Italic']))
                # Page break will happen automatically due to content length
    
    # Add summary at the end
    story.append(Spacer(1, 0.3*inch))
    summary_text = f"""
    <b>Chat Summary:</b><br/>
    Total Messages: {len(chat)}<br/>
    Your Messages: {len([m for m in chat if m.get('role') == 'user'])}<br/>
    Assistant Messages: {len([m for m in chat if m.get('role') == 'assistant'])}<br/>
    Export Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    summary = Paragraph(summary_text, styles['Normal'])
    story.append(summary)
    
    doc.build(story)
    buffer.seek(0)
    return buffer