/**
 * Remark plugin: transforms VitePress `:::` container blocks from the mdast tree.
 */
import { visit } from 'unist-util-visit';

const VALID_TYPES = new Set(['tip', 'info', 'warning', 'details']);

function extractText(node) {
  const n = node;
  if (n.type === 'text' && typeof n.value === 'string') return n.value;
  if (n.children) return n.children.map(extractText).join('');
  return '';
}

/**
 * Handle a single paragraph that contains both a ::: open and close fence.
 */
function splitParagraphWithFences(para, index, parent) {
  const fullText = extractText(para);
  if (!fullText.includes(':::')) return;

  const lines = fullText.split('\n');
  const segments = [];
  let currentContent = [];
  let inFence = false;
  let fenceType = '';
  let fenceTitle = '';
  let fenceLines = [];

  for (const line of lines) {
    const openMatch = line.match(/^:::\s*(\w+)\s*(.*)/);
    const closeMatch = line.match(/^:::$/);

    if (openMatch && VALID_TYPES.has(openMatch[1]) && !inFence) {
      if (currentContent.length > 0) {
        segments.push({ type: 'content', value: currentContent.join('\n') });
        currentContent = [];
      }
      inFence = true;
      fenceType = openMatch[1];
      fenceTitle = openMatch[2].trim();
      fenceLines = [];
    } else if (closeMatch && inFence) {
      const body = fenceLines.join('\n');
      let openHtml, closeHtml;

      if (fenceType === 'details') {
        const isOpen = /\{open\}/.test(fenceTitle);
        fenceTitle = fenceTitle.replace(/\s*\{open\}\s*/g, '').trim();
        openHtml = `<details${isOpen ? ' open' : ''}><summary>${fenceTitle}</summary>`;
        closeHtml = '</details>';
      } else {
        openHtml = `<div class="custom-block ${fenceType}"><p class="custom-block-title">${fenceTitle}</p>`;
        closeHtml = '</div>';
      }

      segments.push({ type: 'html', value: openHtml + '\n' + body + '\n' + closeHtml });
      inFence = false;
    } else if (inFence) {
      fenceLines.push(line);
    } else {
      currentContent.push(line);
    }
  }

  if (inFence) {
    currentContent.push(...fenceLines);
  }
  if (currentContent.length > 0) {
    segments.push({ type: 'content', value: currentContent.join('\n') });
  }

  // No change
  if (segments.length === 1 && segments[0].type === 'content') return;

  const replacements = [];
  for (const seg of segments) {
    if (seg.type === 'html') {
      replacements.push({ type: 'html', value: seg.value });
    } else {
      const trimmed = seg.value.trim();
      if (trimmed) {
        replacements.push({ type: 'paragraph', children: [{ type: 'text', value: trimmed }] });
      }
    }
  }

  if (replacements.length > 0) {
    parent.children.splice(index, 1, ...replacements);
  }
}

/**
 * Handle ::: blocks where open and close fences span multiple top-level nodes.
 */
function handleTopLevelFences(tree) {
  const children = tree.children;

  for (let i = 0; i < children.length; i++) {
    const child = children[i];
    if (child.type !== 'paragraph') continue;

    const text = extractText(child);
    const openMatch = text.match(/^:::\s*(\w+)\s*(.*)/);
    if (!openMatch || !VALID_TYPES.has(openMatch[1])) continue;

    const fenceType = openMatch[1];
    let fenceTitle = openMatch[2].trim();
    const bodyLines = text.split('\n').slice(1);

    // Check if closing ::: is in this same paragraph
    const lastLine = bodyLines[bodyLines.length - 1] || '';
    if (lastLine.trim() === ':::') {
      bodyLines.pop();
      const body = bodyLines.join('\n');

      let openHtml, closeHtml;
      if (fenceType === 'details') {
        const isOpen = /\{open\}/.test(fenceTitle);
        fenceTitle = fenceTitle.replace(/\s*\{open\}\s*/g, '').trim();
        openHtml = `<details${isOpen ? ' open' : ''}><summary>${fenceTitle}</summary>`;
        closeHtml = '</details>';
      } else {
        openHtml = `<div class="custom-block ${fenceType}"><p class="custom-block-title">${fenceTitle}</p>`;
        closeHtml = '</div>';
      }

      const openNode = { type: 'html', value: openHtml };
      const closeNode = { type: 'html', value: closeHtml };

      if (body.trim()) {
        const bodyPara = { type: 'paragraph', children: [{ type: 'text', value: body }] };
        children.splice(i, 1, openNode, bodyPara, closeNode);
      } else {
        children.splice(i, 1, openNode, closeNode);
      }
      continue;
    }

    // Search for closing ::: in subsequent nodes
    let closeIdx = -1;
    let closeIsEmbedded = false;

    for (let j = i + 1; j < children.length; j++) {
      const nextChild = children[j];
      const nextText = extractText(nextChild);

      if (nextText.trim() === ':::') {
        closeIdx = j;
        closeIsEmbedded = false;
        break;
      }

      // ::: embedded at end of paragraph
      if (nextChild.type === 'paragraph') {
        const lines = nextText.split('\n');
        if (lines[lines.length - 1].trim() === ':::') {
          closeIdx = j;
          closeIsEmbedded = true;
          lines.pop();
          const remaining = lines.join('\n').trim();
          if (remaining) {
            nextChild.children = [{ type: 'text', value: remaining }];
          } else {
            children.splice(j, 1);
            closeIdx = j - 1;
            closeIsEmbedded = false;
          }
          break;
        }
      }

      // ::: embedded inside list item
      if (nextChild.type === 'list') {
        const listItems = nextChild.children || [];
        for (const li of listItems) {
          const liText = extractText(li);
          const liLines = liText.split('\n');
          if (liLines[liLines.length - 1].trim() === ':::') {
            closeIdx = j;
            closeIsEmbedded = true;
            if (li.children && li.children.length > 0) {
              const lastPara = li.children[li.children.length - 1];
              if (lastPara.type === 'paragraph' && lastPara.children) {
                const paraText = extractText(lastPara);
                const fixed = paraText.replace(/\n?:::$/, '').trim();
                if (fixed) {
                  lastPara.children = [{ type: 'text', value: fixed }];
                } else {
                  li.children.pop();
                }
              }
            }
            break;
          }
        }
        if (closeIdx !== -1) break;
      }
    }

    if (closeIdx === -1) continue;

    const bodyEnd = closeIsEmbedded ? closeIdx + 1 : closeIdx;
    const bodyChildren = children.slice(i + 1, bodyEnd);
    const spliceCount = bodyEnd - i;

    let openHtml, closeHtml;
    if (fenceType === 'details') {
      const isOpen = /\{open\}/.test(fenceTitle);
      fenceTitle = fenceTitle.replace(/\s*\{open\}\s*/g, '').trim();
      openHtml = `<details${isOpen ? ' open' : ''}><summary>${fenceTitle}</summary>`;
      closeHtml = '</details>';
    } else {
      openHtml = `<div class="custom-block ${fenceType}"><p class="custom-block-title">${fenceTitle}</p>`;
      closeHtml = '</div>';
    }

    const openNode = { type: 'html', value: openHtml };
    const closeNode = { type: 'html', value: closeHtml };

    children.splice(i, spliceCount, openNode, ...bodyChildren, closeNode);
  }
}

export function remarkContainers() {
  return (tree) => {
    // First pass: handle ::: fences embedded within single paragraphs
    visit(tree, 'paragraph', (node, index, parent) => {
      if (!parent || index === undefined) return;
      const text = extractText(node);
      if (!text.includes(':::')) return;

      const lines = text.split('\n');
      const hasOpen = lines.some(l => /^:::\s*\w+/.test(l));
      const hasClose = lines.some(l => l.trim() === ':::');

      if (hasOpen && hasClose) {
        splitParagraphWithFences(node, index, parent);
      }
    });

    // Second pass: handle top-level ::: blocks spanning multiple nodes
    handleTopLevelFences(tree);
  };
}
