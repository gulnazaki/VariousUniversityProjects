	.file	"simplesync.c"
	.text
.Ltext0:
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC0:
	.string	"About to increase variable %d times\n"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC1:
	.string	"mutex_lock"
.LC2:
	.string	"mutex_unlock"
.LC3:
	.string	"Done increasing variable.\n"
	.text
	.p2align 4,,15
	.globl	increase_fn
	.type	increase_fn, @function
increase_fn:
.LFB51:
	.file 1 "simplesync.c"
	.loc 1 40 0
	.cfi_startproc
.LVL0:
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
.LBB12:
.LBB13:
	.file 2 "/usr/include/x86_64-linux-gnu/bits/stdio2.h"
	.loc 2 97 0
	movl	$10000000, %ecx
	movl	$.LC0, %edx
	movl	$1, %esi
	xorl	%eax, %eax
.LBE13:
.LBE12:
	.loc 1 40 0
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	movq	%rdi, %rbp
.LVL1:
.LBB16:
.LBB14:
	.loc 2 97 0
	movq	stderr(%rip), %rdi
.LVL2:
.LBE14:
.LBE16:
	.loc 1 40 0
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
.LBB17:
.LBB15:
	.loc 2 97 0
	movl	$10000000, %ebx
	call	__fprintf_chk
.LVL3:
	.p2align 4,,10
	.p2align 3
.L5:
.LBE15:
.LBE17:
	.loc 1 49 0
	movl	$mutex, %edi
	call	pthread_mutex_lock
.LVL4:
	.loc 1 50 0
	testl	%eax, %eax
	.loc 1 49 0
	movl	%eax, %r12d
.LVL5:
	.loc 1 50 0
	jne	.L8
	.loc 1 54 0
	movl	0(%rbp), %eax
.LVL6:
	.loc 1 55 0
	movl	$mutex, %edi
	.loc 1 54 0
	addl	$1, %eax
	movl	%eax, 0(%rbp)
	.loc 1 55 0
	call	pthread_mutex_unlock
.LVL7:
	.loc 1 56 0
	testl	%eax, %eax
	.loc 1 55 0
	movl	%eax, %r12d
.LVL8:
	.loc 1 56 0
	jne	.L9
.LVL9:
	.loc 1 45 0
	subl	$1, %ebx
.LVL10:
	jne	.L5
.LVL11:
.LBB18:
.LBB19:
	.loc 2 97 0
	movq	stderr(%rip), %rcx
	movl	$26, %edx
	movl	$1, %esi
	movl	$.LC3, %edi
	call	fwrite
.LVL12:
.LBE19:
.LBE18:
	.loc 1 65 0
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 24
.LVL13:
	popq	%rbp
	.cfi_def_cfa_offset 16
.LVL14:
	xorl	%eax, %eax
	popq	%r12
	.cfi_def_cfa_offset 8
.LVL15:
	ret
.LVL16:
.L8:
	.cfi_restore_state
	.loc 1 51 0
	call	__errno_location
.LVL17:
	movl	$.LC1, %edi
	movl	%r12d, (%rax)
	call	perror
.LVL18:
	.loc 1 52 0
	movl	$1, %edi
	call	exit
.LVL19:
.L9:
	.loc 1 57 0
	call	__errno_location
.LVL20:
	movl	$.LC2, %edi
	movl	%r12d, (%rax)
	call	perror
.LVL21:
	.loc 1 58 0
	movl	$1, %edi
	call	exit
.LVL22:
	.cfi_endproc
.LFE51:
	.size	increase_fn, .-increase_fn
	.section	.rodata.str1.8
	.align 8
.LC4:
	.string	"About to decrease variable %d times\n"
	.section	.rodata.str1.1
.LC5:
	.string	"Done decreasing variable.\n"
	.text
	.p2align 4,,15
	.globl	decrease_fn
	.type	decrease_fn, @function
decrease_fn:
.LFB52:
	.loc 1 68 0
	.cfi_startproc
.LVL23:
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
.LBB20:
.LBB21:
	.loc 2 97 0
	movl	$10000000, %ecx
	movl	$.LC4, %edx
	movl	$1, %esi
	xorl	%eax, %eax
.LBE21:
.LBE20:
	.loc 1 68 0
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	movq	%rdi, %rbp
.LVL24:
.LBB24:
.LBB22:
	.loc 2 97 0
	movq	stderr(%rip), %rdi
.LVL25:
.LBE22:
.LBE24:
	.loc 1 68 0
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
.LBB25:
.LBB23:
	.loc 2 97 0
	movl	$10000000, %ebx
	call	__fprintf_chk
.LVL26:
	.p2align 4,,10
	.p2align 3
.L14:
.LBE23:
.LBE25:
	.loc 1 77 0
	movl	$mutex, %edi
	call	pthread_mutex_lock
.LVL27:
	.loc 1 78 0
	testl	%eax, %eax
	.loc 1 77 0
	movl	%eax, %r12d
.LVL28:
	.loc 1 78 0
	jne	.L16
	.loc 1 82 0
	movl	0(%rbp), %eax
.LVL29:
	.loc 1 83 0
	movl	$mutex, %edi
	.loc 1 82 0
	subl	$1, %eax
	movl	%eax, 0(%rbp)
	.loc 1 83 0
	call	pthread_mutex_unlock
.LVL30:
	.loc 1 84 0
	testl	%eax, %eax
	.loc 1 83 0
	movl	%eax, %r12d
.LVL31:
	.loc 1 84 0
	jne	.L17
.LVL32:
	.loc 1 73 0
	subl	$1, %ebx
.LVL33:
	jne	.L14
.LVL34:
.LBB26:
.LBB27:
	.loc 2 97 0
	movq	stderr(%rip), %rcx
	movl	$26, %edx
	movl	$1, %esi
	movl	$.LC5, %edi
	call	fwrite
.LVL35:
.LBE27:
.LBE26:
	.loc 1 93 0
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 24
.LVL36:
	popq	%rbp
	.cfi_def_cfa_offset 16
.LVL37:
	xorl	%eax, %eax
	popq	%r12
	.cfi_def_cfa_offset 8
.LVL38:
	ret
.LVL39:
.L16:
	.cfi_restore_state
	.loc 1 79 0
	call	__errno_location
.LVL40:
	movl	$.LC1, %edi
	movl	%r12d, (%rax)
	call	perror
.LVL41:
	.loc 1 80 0
	movl	$1, %edi
	call	exit
.LVL42:
.L17:
	.loc 1 85 0
	call	__errno_location
.LVL43:
	movl	$.LC2, %edi
	movl	%r12d, (%rax)
	call	perror
.LVL44:
	.loc 1 86 0
	movl	$1, %edi
	call	exit
.LVL45:
	.cfi_endproc
.LFE52:
	.size	decrease_fn, .-decrease_fn
	.section	.rodata.str1.1
.LC6:
	.string	""
.LC7:
	.string	"NOT "
.LC8:
	.string	"pthread_create"
.LC9:
	.string	"pthread_join"
.LC10:
	.string	"%sOK, val = %d.\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB53:
	.loc 1 97 0
	.cfi_startproc
.LVL46:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	.loc 1 109 0
	xorl	%esi, %esi
.LVL47:
	movl	$increase_fn, %edx
	.loc 1 97 0
	subq	$32, %rsp
	.cfi_def_cfa_offset 48
	.loc 1 109 0
	leaq	12(%rsp), %rcx
	leaq	16(%rsp), %rdi
.LVL48:
	.loc 1 104 0
	movl	$0, 12(%rsp)
	.loc 1 109 0
	call	pthread_create
.LVL49:
	.loc 1 110 0
	testl	%eax, %eax
	.loc 1 109 0
	movl	%eax, %ebx
.LVL50:
	.loc 1 110 0
	jne	.L32
	.loc 1 114 0
	leaq	12(%rsp), %rcx
	leaq	24(%rsp), %rdi
	xorl	%esi, %esi
	movl	$decrease_fn, %edx
	call	pthread_create
.LVL51:
	.loc 1 115 0
	testl	%eax, %eax
	.loc 1 114 0
	movl	%eax, %ebx
.LVL52:
	.loc 1 115 0
	jne	.L32
	.loc 1 123 0
	movq	16(%rsp), %rdi
	xorl	%esi, %esi
	call	pthread_join
.LVL53:
	.loc 1 124 0
	testl	%eax, %eax
	.loc 1 123 0
	movl	%eax, %ebx
.LVL54:
	.loc 1 124 0
	jne	.L33
.LVL55:
.L21:
	.loc 1 126 0
	movq	24(%rsp), %rdi
	xorl	%esi, %esi
	call	pthread_join
.LVL56:
	.loc 1 127 0
	testl	%eax, %eax
	.loc 1 126 0
	movl	%eax, %ebx
.LVL57:
	.loc 1 127 0
	jne	.L34
.LVL58:
.L22:
	.loc 1 133 0
	movl	12(%rsp), %ecx
	xorl	%ebx, %ebx
.LVL59:
	.loc 1 135 0
	movl	$.LC7, %eax
	movl	$.LC6, %edx
.LBB28:
.LBB29:
	.loc 2 104 0
	movl	$.LC10, %esi
	movl	$1, %edi
.LBE29:
.LBE28:
	.loc 1 133 0
	testl	%ecx, %ecx
	sete	%bl
.LVL60:
	.loc 1 135 0
	testl	%ebx, %ebx
	cmove	%rax, %rdx
.LVL61:
.LBB31:
.LBB30:
	.loc 2 104 0
	xorl	%eax, %eax
	call	__printf_chk
.LVL62:
.LBE30:
.LBE31:
	.loc 1 138 0
	addq	$32, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 16
	movl	%ebx, %eax
	popq	%rbx
	.cfi_def_cfa_offset 8
.LVL63:
	ret
.LVL64:
.L33:
	.cfi_restore_state
	.loc 1 125 0
	call	__errno_location
.LVL65:
	movl	$.LC9, %edi
	movl	%ebx, (%rax)
	call	perror
.LVL66:
	jmp	.L21
.LVL67:
.L34:
	.loc 1 128 0
	call	__errno_location
.LVL68:
	movl	$.LC9, %edi
	movl	%ebx, (%rax)
	call	perror
.LVL69:
	jmp	.L22
.LVL70:
.L32:
	.loc 1 116 0
	call	__errno_location
.LVL71:
	movl	$.LC8, %edi
	movl	%ebx, (%rax)
	call	perror
.LVL72:
	.loc 1 117 0
	movl	$1, %edi
	call	exit
.LVL73:
	.cfi_endproc
.LFE53:
	.size	main, .-main
	.globl	mutex
	.bss
	.align 32
	.type	mutex, @object
	.size	mutex, 40
mutex:
	.zero	40
	.text
.Letext0:
	.file 3 "/usr/lib/gcc/x86_64-linux-gnu/4.8/include/stddef.h"
	.file 4 "/usr/include/x86_64-linux-gnu/bits/types.h"
	.file 5 "/usr/include/stdio.h"
	.file 6 "/usr/include/libio.h"
	.file 7 "/usr/include/x86_64-linux-gnu/bits/pthreadtypes.h"
	.file 8 "<built-in>"
	.file 9 "/usr/include/pthread.h"
	.file 10 "/usr/include/stdlib.h"
	.file 11 "/usr/include/x86_64-linux-gnu/bits/errno.h"
	.section	.debug_info,"",@progbits
.Ldebug_info0:
	.long	0xb29
	.value	0x4
	.long	.Ldebug_abbrev0
	.byte	0x8
	.uleb128 0x1
	.long	.LASF90
	.byte	0x1
	.long	.LASF91
	.long	.LASF92
	.long	.Ldebug_ranges0+0xb0
	.quad	0
	.long	.Ldebug_line0
	.uleb128 0x2
	.long	.LASF7
	.byte	0x3
	.byte	0xd4
	.long	0x34
	.uleb128 0x3
	.byte	0x8
	.byte	0x7
	.long	.LASF0
	.uleb128 0x3
	.byte	0x1
	.byte	0x8
	.long	.LASF1
	.uleb128 0x3
	.byte	0x2
	.byte	0x7
	.long	.LASF2
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.long	.LASF3
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.long	.LASF4
	.uleb128 0x3
	.byte	0x2
	.byte	0x5
	.long	.LASF5
	.uleb128 0x4
	.byte	0x4
	.byte	0x5
	.string	"int"
	.uleb128 0x3
	.byte	0x8
	.byte	0x5
	.long	.LASF6
	.uleb128 0x2
	.long	.LASF8
	.byte	0x4
	.byte	0x83
	.long	0x65
	.uleb128 0x2
	.long	.LASF9
	.byte	0x4
	.byte	0x84
	.long	0x65
	.uleb128 0x3
	.byte	0x8
	.byte	0x7
	.long	.LASF10
	.uleb128 0x5
	.byte	0x8
	.uleb128 0x6
	.byte	0x8
	.long	0x91
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.long	.LASF11
	.uleb128 0x2
	.long	.LASF12
	.byte	0x5
	.byte	0x30
	.long	0xa3
	.uleb128 0x7
	.long	.LASF42
	.byte	0xd8
	.byte	0x6
	.byte	0xf5
	.long	0x223
	.uleb128 0x8
	.long	.LASF13
	.byte	0x6
	.byte	0xf6
	.long	0x5e
	.byte	0
	.uleb128 0x8
	.long	.LASF14
	.byte	0x6
	.byte	0xfb
	.long	0x8b
	.byte	0x8
	.uleb128 0x8
	.long	.LASF15
	.byte	0x6
	.byte	0xfc
	.long	0x8b
	.byte	0x10
	.uleb128 0x8
	.long	.LASF16
	.byte	0x6
	.byte	0xfd
	.long	0x8b
	.byte	0x18
	.uleb128 0x8
	.long	.LASF17
	.byte	0x6
	.byte	0xfe
	.long	0x8b
	.byte	0x20
	.uleb128 0x8
	.long	.LASF18
	.byte	0x6
	.byte	0xff
	.long	0x8b
	.byte	0x28
	.uleb128 0x9
	.long	.LASF19
	.byte	0x6
	.value	0x100
	.long	0x8b
	.byte	0x30
	.uleb128 0x9
	.long	.LASF20
	.byte	0x6
	.value	0x101
	.long	0x8b
	.byte	0x38
	.uleb128 0x9
	.long	.LASF21
	.byte	0x6
	.value	0x102
	.long	0x8b
	.byte	0x40
	.uleb128 0x9
	.long	.LASF22
	.byte	0x6
	.value	0x104
	.long	0x8b
	.byte	0x48
	.uleb128 0x9
	.long	.LASF23
	.byte	0x6
	.value	0x105
	.long	0x8b
	.byte	0x50
	.uleb128 0x9
	.long	.LASF24
	.byte	0x6
	.value	0x106
	.long	0x8b
	.byte	0x58
	.uleb128 0x9
	.long	.LASF25
	.byte	0x6
	.value	0x108
	.long	0x25b
	.byte	0x60
	.uleb128 0x9
	.long	.LASF26
	.byte	0x6
	.value	0x10a
	.long	0x261
	.byte	0x68
	.uleb128 0x9
	.long	.LASF27
	.byte	0x6
	.value	0x10c
	.long	0x5e
	.byte	0x70
	.uleb128 0x9
	.long	.LASF28
	.byte	0x6
	.value	0x110
	.long	0x5e
	.byte	0x74
	.uleb128 0x9
	.long	.LASF29
	.byte	0x6
	.value	0x112
	.long	0x6c
	.byte	0x78
	.uleb128 0x9
	.long	.LASF30
	.byte	0x6
	.value	0x116
	.long	0x42
	.byte	0x80
	.uleb128 0x9
	.long	.LASF31
	.byte	0x6
	.value	0x117
	.long	0x50
	.byte	0x82
	.uleb128 0x9
	.long	.LASF32
	.byte	0x6
	.value	0x118
	.long	0x267
	.byte	0x83
	.uleb128 0x9
	.long	.LASF33
	.byte	0x6
	.value	0x11c
	.long	0x277
	.byte	0x88
	.uleb128 0x9
	.long	.LASF34
	.byte	0x6
	.value	0x125
	.long	0x77
	.byte	0x90
	.uleb128 0x9
	.long	.LASF35
	.byte	0x6
	.value	0x12e
	.long	0x89
	.byte	0x98
	.uleb128 0x9
	.long	.LASF36
	.byte	0x6
	.value	0x12f
	.long	0x89
	.byte	0xa0
	.uleb128 0x9
	.long	.LASF37
	.byte	0x6
	.value	0x130
	.long	0x89
	.byte	0xa8
	.uleb128 0x9
	.long	.LASF38
	.byte	0x6
	.value	0x131
	.long	0x89
	.byte	0xb0
	.uleb128 0x9
	.long	.LASF39
	.byte	0x6
	.value	0x132
	.long	0x29
	.byte	0xb8
	.uleb128 0x9
	.long	.LASF40
	.byte	0x6
	.value	0x134
	.long	0x5e
	.byte	0xc0
	.uleb128 0x9
	.long	.LASF41
	.byte	0x6
	.value	0x136
	.long	0x27d
	.byte	0xc4
	.byte	0
	.uleb128 0xa
	.long	.LASF93
	.byte	0x6
	.byte	0x9a
	.uleb128 0x7
	.long	.LASF43
	.byte	0x18
	.byte	0x6
	.byte	0xa0
	.long	0x25b
	.uleb128 0x8
	.long	.LASF44
	.byte	0x6
	.byte	0xa1
	.long	0x25b
	.byte	0
	.uleb128 0x8
	.long	.LASF45
	.byte	0x6
	.byte	0xa2
	.long	0x261
	.byte	0x8
	.uleb128 0x8
	.long	.LASF46
	.byte	0x6
	.byte	0xa6
	.long	0x5e
	.byte	0x10
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x22a
	.uleb128 0x6
	.byte	0x8
	.long	0xa3
	.uleb128 0xb
	.long	0x91
	.long	0x277
	.uleb128 0xc
	.long	0x82
	.byte	0
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x223
	.uleb128 0xb
	.long	0x91
	.long	0x28d
	.uleb128 0xc
	.long	0x82
	.byte	0x13
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x293
	.uleb128 0xd
	.long	0x91
	.uleb128 0x6
	.byte	0x8
	.long	0x5e
	.uleb128 0x3
	.byte	0x8
	.byte	0x5
	.long	.LASF47
	.uleb128 0x2
	.long	.LASF48
	.byte	0x7
	.byte	0x3c
	.long	0x34
	.uleb128 0xe
	.long	.LASF51
	.byte	0x38
	.byte	0x7
	.byte	0x3f
	.long	0x2d3
	.uleb128 0xf
	.long	.LASF49
	.byte	0x7
	.byte	0x41
	.long	0x2d3
	.uleb128 0xf
	.long	.LASF50
	.byte	0x7
	.byte	0x42
	.long	0x65
	.byte	0
	.uleb128 0xb
	.long	0x91
	.long	0x2e3
	.uleb128 0xc
	.long	0x82
	.byte	0x37
	.byte	0
	.uleb128 0x2
	.long	.LASF51
	.byte	0x7
	.byte	0x45
	.long	0x2b0
	.uleb128 0x7
	.long	.LASF52
	.byte	0x10
	.byte	0x7
	.byte	0x4b
	.long	0x313
	.uleb128 0x8
	.long	.LASF53
	.byte	0x7
	.byte	0x4d
	.long	0x313
	.byte	0
	.uleb128 0x8
	.long	.LASF54
	.byte	0x7
	.byte	0x4e
	.long	0x313
	.byte	0x8
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x2ee
	.uleb128 0x2
	.long	.LASF55
	.byte	0x7
	.byte	0x4f
	.long	0x2ee
	.uleb128 0x7
	.long	.LASF56
	.byte	0x28
	.byte	0x7
	.byte	0x5c
	.long	0x391
	.uleb128 0x8
	.long	.LASF57
	.byte	0x7
	.byte	0x5e
	.long	0x5e
	.byte	0
	.uleb128 0x8
	.long	.LASF58
	.byte	0x7
	.byte	0x5f
	.long	0x49
	.byte	0x4
	.uleb128 0x8
	.long	.LASF59
	.byte	0x7
	.byte	0x60
	.long	0x5e
	.byte	0x8
	.uleb128 0x8
	.long	.LASF60
	.byte	0x7
	.byte	0x62
	.long	0x49
	.byte	0xc
	.uleb128 0x8
	.long	.LASF61
	.byte	0x7
	.byte	0x66
	.long	0x5e
	.byte	0x10
	.uleb128 0x8
	.long	.LASF62
	.byte	0x7
	.byte	0x68
	.long	0x57
	.byte	0x14
	.uleb128 0x8
	.long	.LASF63
	.byte	0x7
	.byte	0x69
	.long	0x57
	.byte	0x16
	.uleb128 0x8
	.long	.LASF64
	.byte	0x7
	.byte	0x6a
	.long	0x319
	.byte	0x18
	.byte	0
	.uleb128 0x10
	.byte	0x28
	.byte	0x7
	.byte	0x5a
	.long	0x3bb
	.uleb128 0xf
	.long	.LASF65
	.byte	0x7
	.byte	0x7c
	.long	0x324
	.uleb128 0xf
	.long	.LASF49
	.byte	0x7
	.byte	0x7d
	.long	0x3bb
	.uleb128 0xf
	.long	.LASF50
	.byte	0x7
	.byte	0x7e
	.long	0x65
	.byte	0
	.uleb128 0xb
	.long	0x91
	.long	0x3cb
	.uleb128 0xc
	.long	0x82
	.byte	0x27
	.byte	0
	.uleb128 0x2
	.long	.LASF66
	.byte	0x7
	.byte	0x7f
	.long	0x391
	.uleb128 0x3
	.byte	0x8
	.byte	0x7
	.long	.LASF67
	.uleb128 0x11
	.long	0x5e
	.uleb128 0x6
	.byte	0x8
	.long	0x3e8
	.uleb128 0x12
	.uleb128 0x13
	.long	.LASF70
	.byte	0x2
	.byte	0x5f
	.long	0x5e
	.byte	0x3
	.long	0x411
	.uleb128 0x14
	.long	.LASF68
	.byte	0x2
	.byte	0x5f
	.long	0x411
	.uleb128 0x14
	.long	.LASF69
	.byte	0x2
	.byte	0x5f
	.long	0x28d
	.uleb128 0x15
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x98
	.uleb128 0x13
	.long	.LASF71
	.byte	0x2
	.byte	0x66
	.long	0x5e
	.byte	0x3
	.long	0x434
	.uleb128 0x14
	.long	.LASF69
	.byte	0x2
	.byte	0x66
	.long	0x28d
	.uleb128 0x15
	.byte	0
	.uleb128 0x16
	.long	.LASF72
	.byte	0x1
	.byte	0x27
	.long	0x89
	.quad	.LFB51
	.quad	.LFE51-.LFB51
	.uleb128 0x1
	.byte	0x9c
	.long	0x5f1
	.uleb128 0x17
	.string	"arg"
	.byte	0x1
	.byte	0x27
	.long	0x89
	.long	.LLST0
	.uleb128 0x18
	.string	"i"
	.byte	0x1
	.byte	0x29
	.long	0x5e
	.long	.LLST1
	.uleb128 0x18
	.string	"ret"
	.byte	0x1
	.byte	0x29
	.long	0x5e
	.long	.LLST2
	.uleb128 0x18
	.string	"ip"
	.byte	0x1
	.byte	0x2a
	.long	0x5f1
	.long	.LLST3
	.uleb128 0x19
	.long	0x3e9
	.quad	.LBB12
	.long	.Ldebug_ranges0+0
	.byte	0x1
	.byte	0x2c
	.long	0x4e1
	.uleb128 0x1a
	.long	0x404
	.uleb128 0xa
	.byte	0x3
	.quad	.LC0
	.byte	0x9f
	.uleb128 0x1b
	.long	0x3f9
	.uleb128 0x1c
	.quad	.LVL3
	.long	0x9fd
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x31
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x51
	.uleb128 0x9
	.byte	0x3
	.quad	.LC0
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x52
	.uleb128 0x2
	.byte	0x73
	.sleb128 0
	.byte	0
	.byte	0
	.uleb128 0x1e
	.long	0x3e9
	.quad	.LBB18
	.quad	.LBE18-.LBB18
	.byte	0x1
	.byte	0x3e
	.long	0x530
	.uleb128 0x1f
	.long	0x404
	.long	.LLST4
	.uleb128 0x1b
	.long	0x3f9
	.uleb128 0x1c
	.quad	.LVL12
	.long	0xa1d
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC3
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x31
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x51
	.uleb128 0x1
	.byte	0x4a
	.byte	0
	.byte	0
	.uleb128 0x20
	.quad	.LVL4
	.long	0xa45
	.long	0x54f
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	mutex
	.byte	0
	.uleb128 0x20
	.quad	.LVL7
	.long	0xa61
	.long	0x56e
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	mutex
	.byte	0
	.uleb128 0x21
	.quad	.LVL17
	.long	0xa77
	.uleb128 0x20
	.quad	.LVL18
	.long	0xa82
	.long	0x59a
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC1
	.byte	0
	.uleb128 0x20
	.quad	.LVL19
	.long	0xa94
	.long	0x5b1
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x1
	.byte	0x31
	.byte	0
	.uleb128 0x21
	.quad	.LVL20
	.long	0xa77
	.uleb128 0x20
	.quad	.LVL21
	.long	0xa82
	.long	0x5dd
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC2
	.byte	0
	.uleb128 0x1c
	.quad	.LVL22
	.long	0xa94
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x1
	.byte	0x31
	.byte	0
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x3dd
	.uleb128 0x16
	.long	.LASF73
	.byte	0x1
	.byte	0x43
	.long	0x89
	.quad	.LFB52
	.quad	.LFE52-.LFB52
	.uleb128 0x1
	.byte	0x9c
	.long	0x7b4
	.uleb128 0x17
	.string	"arg"
	.byte	0x1
	.byte	0x43
	.long	0x89
	.long	.LLST5
	.uleb128 0x18
	.string	"i"
	.byte	0x1
	.byte	0x45
	.long	0x5e
	.long	.LLST6
	.uleb128 0x18
	.string	"ret"
	.byte	0x1
	.byte	0x45
	.long	0x5e
	.long	.LLST7
	.uleb128 0x18
	.string	"ip"
	.byte	0x1
	.byte	0x46
	.long	0x5f1
	.long	.LLST8
	.uleb128 0x19
	.long	0x3e9
	.quad	.LBB20
	.long	.Ldebug_ranges0+0x40
	.byte	0x1
	.byte	0x48
	.long	0x6a4
	.uleb128 0x1a
	.long	0x404
	.uleb128 0xa
	.byte	0x3
	.quad	.LC4
	.byte	0x9f
	.uleb128 0x1b
	.long	0x3f9
	.uleb128 0x1c
	.quad	.LVL26
	.long	0x9fd
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x31
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x51
	.uleb128 0x9
	.byte	0x3
	.quad	.LC4
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x52
	.uleb128 0x2
	.byte	0x73
	.sleb128 0
	.byte	0
	.byte	0
	.uleb128 0x1e
	.long	0x3e9
	.quad	.LBB26
	.quad	.LBE26-.LBB26
	.byte	0x1
	.byte	0x5a
	.long	0x6f3
	.uleb128 0x1f
	.long	0x404
	.long	.LLST9
	.uleb128 0x1b
	.long	0x3f9
	.uleb128 0x1c
	.quad	.LVL35
	.long	0xa1d
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC5
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x31
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x51
	.uleb128 0x1
	.byte	0x4a
	.byte	0
	.byte	0
	.uleb128 0x20
	.quad	.LVL27
	.long	0xa45
	.long	0x712
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	mutex
	.byte	0
	.uleb128 0x20
	.quad	.LVL30
	.long	0xa61
	.long	0x731
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	mutex
	.byte	0
	.uleb128 0x21
	.quad	.LVL40
	.long	0xa77
	.uleb128 0x20
	.quad	.LVL41
	.long	0xa82
	.long	0x75d
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC1
	.byte	0
	.uleb128 0x20
	.quad	.LVL42
	.long	0xa94
	.long	0x774
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x1
	.byte	0x31
	.byte	0
	.uleb128 0x21
	.quad	.LVL43
	.long	0xa77
	.uleb128 0x20
	.quad	.LVL44
	.long	0xa82
	.long	0x7a0
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC2
	.byte	0
	.uleb128 0x1c
	.quad	.LVL45
	.long	0xa94
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x1
	.byte	0x31
	.byte	0
	.byte	0
	.uleb128 0x16
	.long	.LASF74
	.byte	0x1
	.byte	0x60
	.long	0x5e
	.quad	.LFB53
	.quad	.LFE53-.LFB53
	.uleb128 0x1
	.byte	0x9c
	.long	0x9c1
	.uleb128 0x22
	.long	.LASF75
	.byte	0x1
	.byte	0x60
	.long	0x5e
	.long	.LLST10
	.uleb128 0x22
	.long	.LASF76
	.byte	0x1
	.byte	0x60
	.long	0x9c1
	.long	.LLST11
	.uleb128 0x23
	.string	"val"
	.byte	0x1
	.byte	0x62
	.long	0x5e
	.uleb128 0x2
	.byte	0x91
	.sleb128 -36
	.uleb128 0x18
	.string	"ret"
	.byte	0x1
	.byte	0x62
	.long	0x5e
	.long	.LLST12
	.uleb128 0x18
	.string	"ok"
	.byte	0x1
	.byte	0x62
	.long	0x5e
	.long	.LLST13
	.uleb128 0x23
	.string	"t1"
	.byte	0x1
	.byte	0x63
	.long	0x2a5
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x23
	.string	"t2"
	.byte	0x1
	.byte	0x63
	.long	0x2a5
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x19
	.long	0x417
	.quad	.LBB28
	.long	.Ldebug_ranges0+0x80
	.byte	0x1
	.byte	0x87
	.long	0x89b
	.uleb128 0x1f
	.long	0x427
	.long	.LLST14
	.uleb128 0x1c
	.quad	.LVL62
	.long	0xaa6
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x1
	.byte	0x31
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x9
	.byte	0x3
	.quad	.LC10
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x51
	.uleb128 0x1e
	.byte	0x3
	.quad	.LC7
	.byte	0x3
	.quad	.LC6
	.byte	0x73
	.sleb128 0
	.byte	0x8
	.byte	0x20
	.byte	0x24
	.byte	0x30
	.byte	0x29
	.byte	0x28
	.value	0x1
	.byte	0x16
	.byte	0x13
	.byte	0
	.byte	0
	.uleb128 0x20
	.quad	.LVL49
	.long	0xac1
	.long	0x8cb
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x30
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x51
	.uleb128 0x9
	.byte	0x3
	.quad	increase_fn
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x52
	.uleb128 0x2
	.byte	0x91
	.sleb128 -36
	.byte	0
	.uleb128 0x20
	.quad	.LVL51
	.long	0xac1
	.long	0x8fb
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x30
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x51
	.uleb128 0x9
	.byte	0x3
	.quad	decrease_fn
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x52
	.uleb128 0x2
	.byte	0x91
	.sleb128 -36
	.byte	0
	.uleb128 0x20
	.quad	.LVL53
	.long	0xb0b
	.long	0x912
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x30
	.byte	0
	.uleb128 0x20
	.quad	.LVL56
	.long	0xb0b
	.long	0x929
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x54
	.uleb128 0x1
	.byte	0x30
	.byte	0
	.uleb128 0x21
	.quad	.LVL65
	.long	0xa77
	.uleb128 0x20
	.quad	.LVL66
	.long	0xa82
	.long	0x955
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC9
	.byte	0
	.uleb128 0x21
	.quad	.LVL68
	.long	0xa77
	.uleb128 0x20
	.quad	.LVL69
	.long	0xa82
	.long	0x981
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC9
	.byte	0
	.uleb128 0x21
	.quad	.LVL71
	.long	0xa77
	.uleb128 0x20
	.quad	.LVL72
	.long	0xa82
	.long	0x9ad
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x9
	.byte	0x3
	.quad	.LC8
	.byte	0
	.uleb128 0x1c
	.quad	.LVL73
	.long	0xa94
	.uleb128 0x1d
	.uleb128 0x1
	.byte	0x55
	.uleb128 0x1
	.byte	0x31
	.byte	0
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x8b
	.uleb128 0x24
	.long	.LASF77
	.byte	0x5
	.byte	0xa8
	.long	0x261
	.uleb128 0x24
	.long	.LASF78
	.byte	0x5
	.byte	0xa9
	.long	0x261
	.uleb128 0x24
	.long	.LASF79
	.byte	0x5
	.byte	0xaa
	.long	0x261
	.uleb128 0x25
	.long	.LASF80
	.byte	0x1
	.byte	0x25
	.long	0x3cb
	.uleb128 0x9
	.byte	0x3
	.quad	mutex
	.uleb128 0x26
	.long	.LASF82
	.byte	0x2
	.byte	0x55
	.long	0x5e
	.long	0xa1d
	.uleb128 0x27
	.long	0x411
	.uleb128 0x27
	.long	0x5e
	.uleb128 0x27
	.long	0x28d
	.uleb128 0x15
	.byte	0
	.uleb128 0x28
	.long	.LASF81
	.byte	0x8
	.byte	0
	.long	.LASF94
	.long	0x34
	.long	0xa45
	.uleb128 0x27
	.long	0x3e2
	.uleb128 0x27
	.long	0x34
	.uleb128 0x27
	.long	0x34
	.uleb128 0x27
	.long	0x89
	.byte	0
	.uleb128 0x29
	.long	.LASF83
	.byte	0x9
	.value	0x305
	.long	0x5e
	.long	0xa5b
	.uleb128 0x27
	.long	0xa5b
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x3cb
	.uleb128 0x29
	.long	.LASF84
	.byte	0x9
	.value	0x310
	.long	0x5e
	.long	0xa77
	.uleb128 0x27
	.long	0xa5b
	.byte	0
	.uleb128 0x2a
	.long	.LASF95
	.byte	0xb
	.byte	0x32
	.long	0x298
	.uleb128 0x2b
	.long	.LASF85
	.byte	0x5
	.value	0x34e
	.long	0xa94
	.uleb128 0x27
	.long	0x28d
	.byte	0
	.uleb128 0x2b
	.long	.LASF86
	.byte	0xa
	.value	0x21f
	.long	0xaa6
	.uleb128 0x27
	.long	0x5e
	.byte	0
	.uleb128 0x26
	.long	.LASF87
	.byte	0x2
	.byte	0x57
	.long	0x5e
	.long	0xac1
	.uleb128 0x27
	.long	0x5e
	.uleb128 0x27
	.long	0x28d
	.uleb128 0x15
	.byte	0
	.uleb128 0x26
	.long	.LASF88
	.byte	0x9
	.byte	0xf4
	.long	0x5e
	.long	0xae5
	.uleb128 0x27
	.long	0xae5
	.uleb128 0x27
	.long	0xaeb
	.uleb128 0x27
	.long	0xaf6
	.uleb128 0x27
	.long	0x89
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x2a5
	.uleb128 0x6
	.byte	0x8
	.long	0xaf1
	.uleb128 0xd
	.long	0x2e3
	.uleb128 0x6
	.byte	0x8
	.long	0xafc
	.uleb128 0x2c
	.long	0x89
	.long	0xb0b
	.uleb128 0x27
	.long	0x89
	.byte	0
	.uleb128 0x29
	.long	.LASF89
	.byte	0x9
	.value	0x105
	.long	0x5e
	.long	0xb26
	.uleb128 0x27
	.long	0x2a5
	.uleb128 0x27
	.long	0xb26
	.byte	0
	.uleb128 0x6
	.byte	0x8
	.long	0x89
	.byte	0
	.section	.debug_abbrev,"",@progbits
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0xe
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x1b
	.uleb128 0xe
	.uleb128 0x55
	.uleb128 0x17
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x1
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xc
	.uleb128 0x21
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2f
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0xd
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xe
	.uleb128 0x17
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xf
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x10
	.uleb128 0x17
	.byte	0x1
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x11
	.uleb128 0x35
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x12
	.uleb128 0x26
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x13
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x20
	.uleb128 0xb
	.uleb128 0x34
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x14
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x15
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x16
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x2117
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x17
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x18
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x19
	.uleb128 0x1d
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x52
	.uleb128 0x1
	.uleb128 0x55
	.uleb128 0x17
	.uleb128 0x58
	.uleb128 0xb
	.uleb128 0x59
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1a
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x1b
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1c
	.uleb128 0x4109
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x31
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1d
	.uleb128 0x410a
	.byte	0
	.uleb128 0x2
	.uleb128 0x18
	.uleb128 0x2111
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x1e
	.uleb128 0x1d
	.byte	0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x58
	.uleb128 0xb
	.uleb128 0x59
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1f
	.uleb128 0x5
	.byte	0
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x20
	.uleb128 0x4109
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x31
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x21
	.uleb128 0x4109
	.byte	0
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x31
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x22
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x23
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x24
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x25
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x26
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x27
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x28
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x6e
	.uleb128 0xe
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x29
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2a
	.uleb128 0x2e
	.byte	0
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x2b
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x2c
	.uleb128 0x15
	.byte	0x1
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_loc,"",@progbits
.Ldebug_loc0:
.LLST0:
	.quad	.LVL0
	.quad	.LVL2
	.value	0x1
	.byte	0x55
	.quad	.LVL2
	.quad	.LVL14
	.value	0x1
	.byte	0x56
	.quad	.LVL14
	.quad	.LVL16
	.value	0x4
	.byte	0xf3
	.uleb128 0x1
	.byte	0x55
	.byte	0x9f
	.quad	.LVL16
	.quad	.LFE51
	.value	0x1
	.byte	0x56
	.quad	0
	.quad	0
.LLST1:
	.quad	.LVL3
	.quad	.LVL9
	.value	0x9
	.byte	0xc
	.long	0x989680
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	.LVL9
	.quad	.LVL10
	.value	0x9
	.byte	0xc
	.long	0x989681
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	.LVL10
	.quad	.LVL13
	.value	0x9
	.byte	0xc
	.long	0x989680
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	.LVL16
	.quad	.LFE51
	.value	0x9
	.byte	0xc
	.long	0x989680
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	0
	.quad	0
.LLST2:
	.quad	.LVL5
	.quad	.LVL6
	.value	0x1
	.byte	0x50
	.quad	.LVL6
	.quad	.LVL8
	.value	0x1
	.byte	0x5c
	.quad	.LVL8
	.quad	.LVL12-1
	.value	0x1
	.byte	0x50
	.quad	.LVL12-1
	.quad	.LVL15
	.value	0x1
	.byte	0x5c
	.quad	.LVL16
	.quad	.LVL17-1
	.value	0x1
	.byte	0x50
	.quad	.LVL17-1
	.quad	.LVL19
	.value	0x1
	.byte	0x5c
	.quad	.LVL19
	.quad	.LVL20-1
	.value	0x1
	.byte	0x50
	.quad	.LVL20-1
	.quad	.LFE51
	.value	0x1
	.byte	0x5c
	.quad	0
	.quad	0
.LLST3:
	.quad	.LVL1
	.quad	.LVL2
	.value	0x1
	.byte	0x55
	.quad	.LVL2
	.quad	.LVL14
	.value	0x1
	.byte	0x56
	.quad	.LVL14
	.quad	.LVL16
	.value	0x4
	.byte	0xf3
	.uleb128 0x1
	.byte	0x55
	.byte	0x9f
	.quad	.LVL16
	.quad	.LFE51
	.value	0x1
	.byte	0x56
	.quad	0
	.quad	0
.LLST4:
	.quad	.LVL11
	.quad	.LVL16
	.value	0xa
	.byte	0x3
	.quad	.LC3
	.byte	0x9f
	.quad	0
	.quad	0
.LLST5:
	.quad	.LVL23
	.quad	.LVL25
	.value	0x1
	.byte	0x55
	.quad	.LVL25
	.quad	.LVL37
	.value	0x1
	.byte	0x56
	.quad	.LVL37
	.quad	.LVL39
	.value	0x4
	.byte	0xf3
	.uleb128 0x1
	.byte	0x55
	.byte	0x9f
	.quad	.LVL39
	.quad	.LFE52
	.value	0x1
	.byte	0x56
	.quad	0
	.quad	0
.LLST6:
	.quad	.LVL26
	.quad	.LVL32
	.value	0x9
	.byte	0xc
	.long	0x989680
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	.LVL32
	.quad	.LVL33
	.value	0x9
	.byte	0xc
	.long	0x989681
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	.LVL33
	.quad	.LVL36
	.value	0x9
	.byte	0xc
	.long	0x989680
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	.LVL39
	.quad	.LFE52
	.value	0x9
	.byte	0xc
	.long	0x989680
	.byte	0x73
	.sleb128 0
	.byte	0x1c
	.byte	0x9f
	.quad	0
	.quad	0
.LLST7:
	.quad	.LVL28
	.quad	.LVL29
	.value	0x1
	.byte	0x50
	.quad	.LVL29
	.quad	.LVL31
	.value	0x1
	.byte	0x5c
	.quad	.LVL31
	.quad	.LVL35-1
	.value	0x1
	.byte	0x50
	.quad	.LVL35-1
	.quad	.LVL38
	.value	0x1
	.byte	0x5c
	.quad	.LVL39
	.quad	.LVL40-1
	.value	0x1
	.byte	0x50
	.quad	.LVL40-1
	.quad	.LVL42
	.value	0x1
	.byte	0x5c
	.quad	.LVL42
	.quad	.LVL43-1
	.value	0x1
	.byte	0x50
	.quad	.LVL43-1
	.quad	.LFE52
	.value	0x1
	.byte	0x5c
	.quad	0
	.quad	0
.LLST8:
	.quad	.LVL24
	.quad	.LVL25
	.value	0x1
	.byte	0x55
	.quad	.LVL25
	.quad	.LVL37
	.value	0x1
	.byte	0x56
	.quad	.LVL37
	.quad	.LVL39
	.value	0x4
	.byte	0xf3
	.uleb128 0x1
	.byte	0x55
	.byte	0x9f
	.quad	.LVL39
	.quad	.LFE52
	.value	0x1
	.byte	0x56
	.quad	0
	.quad	0
.LLST9:
	.quad	.LVL34
	.quad	.LVL39
	.value	0xa
	.byte	0x3
	.quad	.LC5
	.byte	0x9f
	.quad	0
	.quad	0
.LLST10:
	.quad	.LVL46
	.quad	.LVL48
	.value	0x1
	.byte	0x55
	.quad	.LVL48
	.quad	.LFE53
	.value	0x4
	.byte	0xf3
	.uleb128 0x1
	.byte	0x55
	.byte	0x9f
	.quad	0
	.quad	0
.LLST11:
	.quad	.LVL46
	.quad	.LVL47
	.value	0x1
	.byte	0x54
	.quad	.LVL47
	.quad	.LFE53
	.value	0x4
	.byte	0xf3
	.uleb128 0x1
	.byte	0x54
	.byte	0x9f
	.quad	0
	.quad	0
.LLST12:
	.quad	.LVL50
	.quad	.LVL51-1
	.value	0x1
	.byte	0x50
	.quad	.LVL51-1
	.quad	.LVL52
	.value	0x1
	.byte	0x53
	.quad	.LVL52
	.quad	.LVL53-1
	.value	0x1
	.byte	0x50
	.quad	.LVL53-1
	.quad	.LVL54
	.value	0x1
	.byte	0x53
	.quad	.LVL54
	.quad	.LVL55
	.value	0x1
	.byte	0x50
	.quad	.LVL55
	.quad	.LVL57
	.value	0x1
	.byte	0x53
	.quad	.LVL57
	.quad	.LVL58
	.value	0x1
	.byte	0x50
	.quad	.LVL58
	.quad	.LVL59
	.value	0x1
	.byte	0x53
	.quad	.LVL64
	.quad	.LVL65-1
	.value	0x1
	.byte	0x50
	.quad	.LVL65-1
	.quad	.LVL67
	.value	0x1
	.byte	0x53
	.quad	.LVL67
	.quad	.LVL68-1
	.value	0x1
	.byte	0x50
	.quad	.LVL68-1
	.quad	.LVL70
	.value	0x1
	.byte	0x53
	.quad	.LVL70
	.quad	.LVL71-1
	.value	0x1
	.byte	0x50
	.quad	.LVL71-1
	.quad	.LFE53
	.value	0x1
	.byte	0x53
	.quad	0
	.quad	0
.LLST13:
	.quad	.LVL60
	.quad	.LVL63
	.value	0x1
	.byte	0x53
	.quad	.LVL63
	.quad	.LVL64
	.value	0x1
	.byte	0x50
	.quad	0
	.quad	0
.LLST14:
	.quad	.LVL61
	.quad	.LVL64
	.value	0xa
	.byte	0x3
	.quad	.LC10
	.byte	0x9f
	.quad	0
	.quad	0
	.section	.debug_aranges,"",@progbits
	.long	0x3c
	.value	0x2
	.long	.Ldebug_info0
	.byte	0x8
	.byte	0
	.value	0
	.value	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	.LFB53
	.quad	.LFE53-.LFB53
	.quad	0
	.quad	0
	.section	.debug_ranges,"",@progbits
.Ldebug_ranges0:
	.quad	.LBB12
	.quad	.LBE12
	.quad	.LBB16
	.quad	.LBE16
	.quad	.LBB17
	.quad	.LBE17
	.quad	0
	.quad	0
	.quad	.LBB20
	.quad	.LBE20
	.quad	.LBB24
	.quad	.LBE24
	.quad	.LBB25
	.quad	.LBE25
	.quad	0
	.quad	0
	.quad	.LBB28
	.quad	.LBE28
	.quad	.LBB31
	.quad	.LBE31
	.quad	0
	.quad	0
	.quad	.Ltext0
	.quad	.Letext0
	.quad	.LFB53
	.quad	.LFE53
	.quad	0
	.quad	0
	.section	.debug_line,"",@progbits
.Ldebug_line0:
	.section	.debug_str,"MS",@progbits,1
.LASF95:
	.string	"__errno_location"
.LASF87:
	.string	"__printf_chk"
.LASF42:
	.string	"_IO_FILE"
.LASF24:
	.string	"_IO_save_end"
.LASF5:
	.string	"short int"
.LASF7:
	.string	"size_t"
.LASF10:
	.string	"sizetype"
.LASF34:
	.string	"_offset"
.LASF52:
	.string	"__pthread_internal_list"
.LASF18:
	.string	"_IO_write_ptr"
.LASF13:
	.string	"_flags"
.LASF66:
	.string	"pthread_mutex_t"
.LASF58:
	.string	"__count"
.LASF33:
	.string	"_lock"
.LASF50:
	.string	"__align"
.LASF25:
	.string	"_markers"
.LASF15:
	.string	"_IO_read_end"
.LASF53:
	.string	"__prev"
.LASF83:
	.string	"pthread_mutex_lock"
.LASF54:
	.string	"__next"
.LASF79:
	.string	"stderr"
.LASF43:
	.string	"_IO_marker"
.LASF47:
	.string	"long long int"
.LASF89:
	.string	"pthread_join"
.LASF77:
	.string	"stdin"
.LASF88:
	.string	"pthread_create"
.LASF6:
	.string	"long int"
.LASF71:
	.string	"printf"
.LASF30:
	.string	"_cur_column"
.LASF85:
	.string	"perror"
.LASF46:
	.string	"_pos"
.LASF70:
	.string	"fprintf"
.LASF62:
	.string	"__spins"
.LASF76:
	.string	"argv"
.LASF86:
	.string	"exit"
.LASF45:
	.string	"_sbuf"
.LASF29:
	.string	"_old_offset"
.LASF81:
	.string	"__builtin_fwrite"
.LASF1:
	.string	"unsigned char"
.LASF75:
	.string	"argc"
.LASF4:
	.string	"signed char"
.LASF67:
	.string	"long long unsigned int"
.LASF3:
	.string	"unsigned int"
.LASF69:
	.string	"__fmt"
.LASF32:
	.string	"_shortbuf"
.LASF17:
	.string	"_IO_write_base"
.LASF41:
	.string	"_unused2"
.LASF14:
	.string	"_IO_read_ptr"
.LASF80:
	.string	"mutex"
.LASF49:
	.string	"__size"
.LASF21:
	.string	"_IO_buf_end"
.LASF11:
	.string	"char"
.LASF60:
	.string	"__nusers"
.LASF74:
	.string	"main"
.LASF91:
	.string	"simplesync.c"
.LASF44:
	.string	"_next"
.LASF35:
	.string	"__pad1"
.LASF36:
	.string	"__pad2"
.LASF37:
	.string	"__pad3"
.LASF38:
	.string	"__pad4"
.LASF39:
	.string	"__pad5"
.LASF84:
	.string	"pthread_mutex_unlock"
.LASF57:
	.string	"__lock"
.LASF59:
	.string	"__owner"
.LASF2:
	.string	"short unsigned int"
.LASF72:
	.string	"increase_fn"
.LASF92:
	.string	"/home/nazgul/Unistuff/os/lab/3/workspace"
.LASF56:
	.string	"__pthread_mutex_s"
.LASF94:
	.string	"fwrite"
.LASF0:
	.string	"long unsigned int"
.LASF19:
	.string	"_IO_write_end"
.LASF9:
	.string	"__off64_t"
.LASF63:
	.string	"__elision"
.LASF27:
	.string	"_fileno"
.LASF26:
	.string	"_chain"
.LASF55:
	.string	"__pthread_list_t"
.LASF73:
	.string	"decrease_fn"
.LASF65:
	.string	"__data"
.LASF8:
	.string	"__off_t"
.LASF23:
	.string	"_IO_backup_base"
.LASF90:
	.string	"GNU C 4.8.5 -mtune=generic -march=x86-64 -g -O2 -fstack-protector"
.LASF20:
	.string	"_IO_buf_base"
.LASF28:
	.string	"_flags2"
.LASF40:
	.string	"_mode"
.LASF16:
	.string	"_IO_read_base"
.LASF68:
	.string	"__stream"
.LASF64:
	.string	"__list"
.LASF31:
	.string	"_vtable_offset"
.LASF22:
	.string	"_IO_save_base"
.LASF82:
	.string	"__fprintf_chk"
.LASF12:
	.string	"FILE"
.LASF61:
	.string	"__kind"
.LASF51:
	.string	"pthread_attr_t"
.LASF48:
	.string	"pthread_t"
.LASF78:
	.string	"stdout"
.LASF93:
	.string	"_IO_lock_t"
	.ident	"GCC: (Ubuntu 4.8.5-2ubuntu1~14.04.1) 4.8.5"
	.section	.note.GNU-stack,"",@progbits
